
import json
import pymongo
from pymongo import MongoClient
import os,sys
import logging
import multiprocessing as mp
import psutil

from inti.MA.MAExecutor import MAExecutor
from inti.MA.MAMetadata import MACollectionNames

class MABase:
    def __init__(self,ma_dir,db_name,collection_names,sep='\t', buffer_size=1024*1024, dburi='mongodb://localhost:27017/',
                 log_file='mabase.log', info_level=logging.DEBUG):
        self.ma_dir = ma_dir
        self.buffer_size = buffer_size
        self.info_level = info_level
        self.log_file = log_file
        self.logger = logging.getLogger(__name__)
        self.set_info_level(info_level)
        self.db_name = db_name
        self.collection_names = collection_names
        self.sep = sep
        self.dburi = dburi

    def process(self,collection_name,line):
        '''
        To be implemented by childrens
        '''
        self.logger.error(
            'ERROR: this method is not implemented yet, it cant be use in the base class')
        sys.exit(1)
        return ""

    def checkpoint_get(self):
        client = MongoClient(self.dburi)
        db = client[self.db_name]
        collection = db["checkpoint"]
        if collection.count_documents({"_id":0}) == 0:
            self.checkpoint_create()
        checkpoint = collection.find_one({'_id':0})
        client.close()
        return checkpoint

    def checkpoint_update(self,ma_dir,collection):
        checkpoint = self.checkpoint_get()
        checkpoint[ma_dir][collection]=1
        client = MongoClient(self.dburi)
        db = client[self.db_name]
        col = db["checkpoint"]
        col.update_one({'_id':0},{"$set":checkpoint})
        client.close()

    def checkpoint_create(self,overwrite=False):
        client = MongoClient(self.dburi)
        db = client[self.db_name]
        collection = db["checkpoint"]
        if collection.count_documents({"_id":0}) == 0 or overwrite:
            print("=== Creating CheckPoint")
            collection.drop()
            reg = {'_id':0}
            for ma_dir in list(MACollectionNames.keys()):
                reg[ma_dir] = {}
                for col in MACollectionNames[ma_dir]:
                    reg[ma_dir][col]=0
            collection.insert_one(reg)
        client.close()

    def resume(self,ma_dir):
        client = MongoClient(self.dburi)
        db = client[self.db_name]
        collection = db["checkpoint"]
        print("=== Resume ")
        for col in MACollectionNames[ma_dir]:
            print("====== {} = {}".format(col,db[col].count_documents({})))
        client.close()


    def checkpoint_clean_collections(self,ma_dir):
        checkpoint = self.checkpoint_get()
        client = MongoClient(self.dburi)
        db = client[self.db_name]
        del checkpoint['_id']
        for collection in checkpoint[ma_dir]:
            if checkpoint[ma_dir][collection] == 0:
                db[collection].drop()
        client.close()


    def create_index(self,collection_name,index):
        self.client = MongoClient(self.dburi)
        self.db = self.client[self.db_name]
        self.collection = self.db[collection_name]
        print('Creating index {} = {}'.format(collection_name,index))
        self.collection.create_index(index)
        self.client.close()

    def create_indexes(self,max_threads=None):
        '''
        To be implemented by childrens
        '''
        self.logger.error(
            'ERROR: this method is not implemented yet, it cant be use in the base class')
        sys.exit(1)
        return ""

    def set_info_level(self, info_level):
        '''
        Information level for debug or verbosity of the application (https://docs.python.org/3.1/library/logging.html)
        '''
        if info_level != logging.DEBUG:
            logging.basicConfig(filename=self.log_file, level=info_level)
        self.info_level = info_level

    def process_wrapper(self,file_name,collection_name,chunkStart, chunkSize):
        self.client = MongoClient(self.dburi)
        self.db = self.client[self.db_name]
        self.collection = self.db[collection_name]

        with open(file_name,'rb') as f:
            f.seek(chunkStart)
            lines = f.read(chunkSize).decode('utf-8').split('\r\n')
            processed_lines = []
            for line in lines:
                line = self.process(collection_name,line)
                if line is not None:
                    processed_lines.append(line)
            self.collection.insert_many(processed_lines,ordered=False)
        self.client.close()

    def chunkify(self,file_name):
        fileEnd = os.path.getsize(file_name)
        with open(file_name,'rb') as f:
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
        '''
        To be implemented by childrens
        '''
        self.logger.error(
            'ERROR: this method is not implemented yet, it cant be use in the base class')
        sys.exit(1)
        return ""
