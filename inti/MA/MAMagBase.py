
import json
import pymongo
from pymongo import MongoClient
import os,sys
import logging
import multiprocessing as mp
import psutil
import bson

from inti.MA.MAMagExecutor import MAMagExecutor

MAMagColTypeLong = ['EstimatedCitation',
 'JournalId',
 'FieldOfStudyId2',
 'AffiliationId',
 'RecommendedPaperId',
 'ConferenceInstanceId',
 'ChildFieldOfStudyId',
 'PaperFamilyCount',
 'AuthorId',
 'PaperCount',
 'FamilyId',
 'PaperId',
 'EntityId',
 'PaperReferenceId',
 'FieldOfStudyId',
 'ReferenceCount',
 'ConferenceSeriesId',
 'RelatedEntityId',
 'FieldOfStudyId1',
 'LastKnownAffiliationId',
 'CitationCount']

MAMagColTypeInt = ['AuthorSequenceNumber',
 'Rank',
 'RelationshipType',
 'Year',
 'ResourceType',
 'FamilyRank',
 'AttributeType',
 'RelatedType',
 'SourceType']

MAMagColTypeFloat = ['Latitude',
'Longitude',
'Score',
'Rank']

MAMagColNames = {}
MAMagColNames['Authors'] = ['AuthorId', 'Rank', 'NormalizedName', 'DisplayName', 'LastKnownAffiliationId', 'PaperCount', 'PaperFamilyCount', 'CitationCount', 'CreatedDate']
MAMagColNames['Authors_indexes'] = ['AuthorId','LastKnownAffiliationId']

MAMagColNames['Affiliations'] = ['AffiliationId', 'Rank', 'NormalizedName', 'DisplayName', 'GridId', 'OfficialPage', 'WikiPage', 'PaperCount', 'PaperFamilyCount', 'CitationCount', 'Latitude', 'Longitude', 'CreatedDate']
MAMagColNames['Affiliations_indexes'] = ['AffiliationId','GridId']

MAMagColNames['PaperAuthorAffiliations'] = ['PaperId', 'AuthorId', 'AffiliationId', 'AuthorSequenceNumber', 'OriginalAuthor', 'OriginalAffiliation']
MAMagColNames['PaperAuthorAffiliations_indexes'] = ['PaperId','AuthorId','AffiliationId'] 

MAMagColNames['Papers'] = ['PaperId', 'Rank', 'Doi', 'DocType', 'PaperTitle', 'OriginalTitle', 'BookTitle', 'Year', 'Date', 'Publisher', 'JournalId', 'ConferenceSeriesId', 'ConferenceInstanceId', 'Volume', 'Issue', 'FirstPage', 'LastPage', 'ReferenceCount', 'CitationCount', 'EstimatedCitation', 'OriginalVenue', 'FamilyId', 'CreatedDate']
MAMagColNames['Papers_indexes'] = ['PaperId','JournalId','ConferenceSeriesId','ConferenceInstanceId','FamilyId']

MAMagColNames['PaperUrls'] = ['PaperId', 'SourceType', 'SourceUrl', 'LanguageCode']
MAMagColNames['PaperUrls_indexes'] = ['PaperId']

MAMagColNames['PaperResources'] = ['PaperId', 'ResourceType', 'ResourceUrl', 'SourceUrl', 'RelationshipType']
MAMagColNames['PaperResources_indexes'] = ['PaperId']

MAMagColNames['PaperReferences'] = ['PaperId', 'PaperReferenceId']
MAMagColNames['PaperReferences_indexes'] = ['PaperId', 'PaperReferenceId']

MAMagColNames['PaperExtendedAttributes'] = ['PaperId', 'AttributeType', 'AttributeValue']
MAMagColNames['PaperExtendedAttributes_indexes'] = ['PaperId']

MAMagColNames['Journals'] = ['JournalId', 'Rank', 'NormalizedName', 'DisplayName', 'Issn', 'Publisher', 'Webpage', 'PaperCount', 'PaperFamilyCount', 'CitationCount', 'CreatedDate']
MAMagColNames['Journals_indexes'] = ['JournalId']

MAMagColNames['ConferenceSeries'] = ['ConferenceSeriesId', 'Rank', 'NormalizedName', 'DisplayName', 'PaperCount', 'PaperFamilyCount', 'CitationCount', 'CreatedDate']
MAMagColNames['ConferenceSeries_indexes'] = ['ConferenceSeriesId']

MAMagColNames['ConferenceInstances'] = ['ConferenceInstanceId', 'NormalizedName', 'DisplayName', 'ConferenceSeriesId', 'Location', 'OfficialUrl', 'StartDate', 'EndDate', 'AbstractRegistrationDate', 'SubmissionDeadlineDate', 'NotificationDueDate', 'FinalVersionDueDate', 'PaperCount', 'PaperFamilyCount', 'CitationCount', 'Latitude', 'Longitude', 'CreatedDate']
MAMagColNames['ConferenceInstances_indexes'] = ['ConferenceInstanceId','ConferenceSeriesId']

class MAMagBase:
    def __init__(self,file_name,database_name,collection,col_names,col_indexes,sep='\t', buffer_size=1024*1024, dburi='mongodb://localhost:27017/', hunabku_server = None, hunabku_apikey = None,
                 log_file='mamagbase.log', info_level=logging.DEBUG):
        self.hunabku_server = hunabku_server
        self.hunabku_apikey = hunabku_apikey
        self.file_name = file_name
        self.buffer_size = buffer_size
        self.info_level = info_level
        self.log_file = log_file
        self.logger = logging.getLogger(__name__)
        self.set_info_level(info_level)
        self.database_name = database_name
        self.collection = None
        self.collection_name = collection
        self.col_names = col_names
        self.col_indexes = col_indexes
        self.sep = sep
        self.dburi = dburi

    def process(self,line):
        register={}
        if type(line) == type(bytes()):
            line = line.decode('utf-8')
        fields = line.split(self.sep)
        if len(fields) == len(self.col_names):
            for index in range(len(self.col_names)):
                col_name = self.col_names[index]
                if col_name in MAMagColTypeLong:
                    value = fields[index].strip()
                    if value == "":
                        value=0                        
                    register[col_name]=bson.int64.Int64(value)
                elif col_name == "Rank" and self.collection_name == "RelatedFieldOfStudy":#the only exception
                    if value == "":
                        value=0.0                        
                    register[col_name]=float(value)
                elif col_name in MAMagColTypeInt:
                    if value == "":
                        value=0                        
                    register[col_name]=bson.int64.Int64(value)
                elif col_name in MAMagColTypeFloat:
                    if value == "":
                        value=0.0                        
                    register[col_name]=float(value)
                else:
                    register[self.col_names[index]]=fields[index]
                
            return register
            #self.collection.insert_one(register)
        else:
            #print(line)
            pass

    def set_info_level(self, info_level):
        '''
        Information level for debug or verbosity of the application (https://docs.python.org/3.1/library/logging.html)
        '''
        if info_level != logging.DEBUG:
            logging.basicConfig(filename=self.log_file, level=info_level)
        self.info_level = info_level

    def process_wrapper(self,chunkStart, chunkSize):
        self.client = MongoClient(self.dburi)
        self.db = self.client[self.database_name]
        self.collection = self.db[self.collection_name]

        with open(self.file_name,'rb') as f:
            f.seek(chunkStart)
            lines = f.read(chunkSize).decode('utf-8').split('\r\n')
            #self.logger.info("Chunk lines = "+str(len(lines)))
            processed_lines = []
            for line in lines:
                line = self.process(line)
                if line is not None:
                    processed_lines.append(line)
            self.collection.insert_many(processed_lines,ordered=False)
        self.client.close()

    def chunkify(self):
        fileEnd = os.path.getsize(self.file_name)
        with open(self.file_name,'rb') as f:
            chunkEnd = f.tell()
            while True:
                chunkStart = chunkEnd
                f.seek(self.buffer_size,1)
                f.readline()
                chunkEnd = f.tell()
                yield chunkStart, chunkEnd - chunkStart
                if chunkEnd > fileEnd:
                    break

    def run(self,max_threads=None):
        MAMagExecutor(self,max_threads=max_threads)
