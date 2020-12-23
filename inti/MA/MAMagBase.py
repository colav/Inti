
import json
import pymongo
from pymongo import MongoClient
import os,sys
import logging
import multiprocessing as mp
import psutil

from inti.MA.MAMagExecutor import MAMagExecutor

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
        self.collection = collection
        self.col_names = col_names
        self.col_indexes = col_indexes
        self.sep = sep


    def process(self,line):
        register={}
        if type(line) == type(bytes()):
            line = line.decode('utf-8')
        fields = line.split(self.sep)
        #print(len(fields),len(self.col_names))
        if len(fields) == len(self.col_names):
            for index in range(len(self.col_names)):
                register[self.col_names[index]]=fields[index]
            self.collection.insert_one(register)
        else:
            print(line)
            pass

    def create_indexes(self):
        print('Creating indexes '+self.col_indexes)
        for index in self.col_indexes:
            self.collection.create_index(index)

    def set_info_level(self, info_level):
        '''
        Information level for debug or verbosity of the application (https://docs.python.org/3.1/library/logging.html)
        '''
        if info_level != logging.DEBUG:
            logging.basicConfig(filename=self.log_file, level=info_level)
        self.info_level = info_level

    def process_wrapper(self,chunkStart, chunkSize):
        with open(self.file_name,'rb') as f:
            f.seek(chunkStart)
            lines = f.read(chunkSize).decode('utf-8').split('\r\n')
            self.logger.info("Chunk lines = "+str(len(lines)))
            for line in lines:
                self.process(line)

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
        self.client = MongoClient()
        self.db = self.client[self.database_name]
        self.collection = self.db[self.collection]
        MAMagExecutor(self,max_threads=max_threads)
        self.client.close()