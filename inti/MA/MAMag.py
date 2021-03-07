from inti.MA.MAMetadata import MAColTypes, MAColumnNames, MACollectionNames 
from inti.MA.MABase import MABase
from inti.MA.MAExecutor import MAExecutor
from joblib import Parallel, delayed
import logging
import psutil
import bson

class MAMag(MABase):
    def __init__(self,ma_dir,database_name,sep='\t', buffer_size=1024*1024, dburi='mongodb://localhost:27017/',
                 log_file='mamagbase.log', info_level=logging.DEBUG):
        """
        The directory should have the next files
        mag/PaperAuthorAffiliations.txt
        mag/ConferenceSeries.txt
        mag/Affiliations.txt
        mag/PaperUrls.txt
        mag/Papers.txt
        mag/PaperResources.txt
        mag/ConferenceInstances.txt
        mag/Authors.txt
        mag/PaperReferences.txt
        mag/PaperExtendedAttributes.txt
        mag/Journals.txt
        """
        super().__init__(ma_dir,database_name,MACollectionNames["mag"],sep, buffer_size, dburi,
                 log_file, info_level)

    def process(self,collection_name,line):
        register={}
        col_names = MAColumnNames["mag"][collection_name]
        #col_indexes = MAColumnNames["mag"]['{}_indexes'.format(collection_name)]
        if type(line) == type(bytes()):
            line = line.decode('utf-8')
        fields = line.split(self.sep)
        if len(fields) == len(col_names):
            for index in range(len(col_names)):
                col_name = col_names[index]
                if col_name in MAColTypes["mag"]["long"]:
                    value = fields[index].strip()
                    if value == "":
                        value=0                        
                    register[col_name]=bson.int64.Int64(value)
                elif col_name == "Rank" and collection_name == "RelatedFieldOfStudy":#the only exception
                    if value == "":
                        value=0.0                        
                    register[col_name]=float(value)
                elif col_name in MAColTypes["mag"]["int"]:
                    if value == "":
                        value=0                        
                    register[col_name]=bson.int64.Int64(value)
                elif col_name in MAColTypes["mag"]["float"]:
                    if value == "":
                        value=0.0                        
                    register[col_name]=float(value)
                else:
                    register[col_names[index]]=fields[index]
                
            return register
        else:
            pass

    def create_indexes(self,max_threads=None):
        indexes = []
        for collection_name in self.collection_names:
            col_indexes = MAColumnNames["mag"]['{}_indexes'.format(collection_name)]
            for index in col_indexes:
                 indexes.append((collection_name,index))
        if max_threads is None:
            jobs = psutil.cpu_count()
        else:
            jobs = max_threads        
        Parallel(n_jobs=jobs)(delayed(self.create_index)(collection_name,index) for collection_name,index in indexes)

    def run(self,max_threads=None):
        """
        Checkpoint not supported!
        """
        for collection in self.collection_names:
            mag_file=self.ma_dir+'mag/{}.txt'.format(collection)
            MAExecutor(self,mag_file,collection,max_threads=max_threads)
