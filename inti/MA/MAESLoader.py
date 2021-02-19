
import json
import os,sys
import logging
import multiprocessing as mp
import psutil

from elasticsearch import Elasticsearch, helpers

from inti.MA.MAMagExecutor import MAMagExecutor

from inti.MA.MAMagBase import MAMagColNames

class MAESLoader:
    def __init__(self,file_name,index_name,field_name,col_names,sep='\t', buffer_size=1024*1024, db_ip='127.0.0.1',db_port=9200,timeout=120,log_file='maesbase.log', info_level=logging.DEBUG):
        self.file_name = file_name
        self.buffer_size = buffer_size
        self.info_level = info_level
        self.log_file = log_file
        self.logger = logging.getLogger(__name__)
        self.set_info_level(info_level)
        self.sep = sep
        self.db_ip = db_ip
        self.db_port = db_port
        self.timeout = timeout
        self.col_names = col_names
        self.field_name = field_name
        self.index_name = index_name

    def process(self,line):
        register={}
        if type(line) == type(bytes()):
            line = line.decode('utf-8')
        fields = line.split(self.sep)
        if len(fields) == len(self.col_names):
            for index in range(len(self.col_names)):
                col_name = self.col_names[index]
                register[col_name]=fields[index]
                
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
        es = Elasticsearch(HOST=self.db_ip, PORT=self.db_port,timeout=self.timeout)
        
        with open(self.file_name,'rb') as f:
            f.seek(chunkStart)
            lines = f.read(chunkSize).decode('utf-8').split('\r\n')
            #self.logger.info("Chunk lines = "+str(len(lines)))
            processed_lines = []
            for line in lines:
                line = self.process(line)
                if line is not None:
                    entry = {"_index": self.index_name,
                             "_id":str(line['PaperId']),
                            "_source": {self.field_name:line[self.field_name]} }
                    processed_lines.append(entry)
        try:
            helpers.bulk(es, processed_lines, refresh=True, request_timeout=self.timeout) 
        except Exception as e:
            # This can happen if the server is restarted or the connection becomes unavilable
            print(str(e))

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

def run(mag_dir,col_name,index_name,field_name,sep='\t', buffer_size=1024*1024, db_ip='127.0.0.1',db_port=9200,timeout=120,max_threads=None):
    mag_file = mag_dir+'/{}.txt'.format(col_name)
    col_names = MAMagColNames[col_name]

    instance = MAESLoader(mag_file,index_name,field_name,col_names,sep, buffer_size, db_ip,db_port,timeout)
    instance.run(max_threads=max_threads)
