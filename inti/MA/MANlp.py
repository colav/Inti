from inti.MA.MAMetadata import MAColTypes, MAColumnNames, MACollectionNames 
from inti.MA.MABase import MABase
from inti.MA.MAExecutor import MAExecutor
from joblib import Parallel, delayed
import logging
import psutil
import bson
import glob
import json

class MANlp(MABase):
    def __init__(self,ma_dir,database_name,sep='\t', buffer_size=1024*1024, dburi='mongodb://localhost:27017/',
                 log_file='manlbase.log', info_level=logging.DEBUG):
        """
        The directory should have the next files
        nlp/PaperAbstractsInvertedIndex.txt.*  
        nlp/PaperCitationContexts.txt
        """
        super().__init__(ma_dir,database_name,MACollectionNames["nlp"],sep, buffer_size, dburi,
                 log_file, info_level)

    def inv_index2text(self,data):
        abstract=[""]*data['IndexLength']
        for key in data["InvertedIndex"]:
            for i in data["InvertedIndex"][key]:
                abstract[i]=key
        return " ".join(abstract)

    def process(self,collection_name,line):
        register={}
        col_names = MAColumnNames["nlp"][collection_name]
        if type(line) == type(bytes()):
            line = line.decode('utf-8')
        fields = line.split(self.sep)
        if len(fields) == len(col_names):
            for index in range(len(col_names)):
                col_name = col_names[index]
                if col_name in MAColTypes["nlp"]["long"]:
                    value = fields[index].strip()
                    if value == "":
                        value=0                        
                    register[col_name]=bson.int64.Int64(value)
                else:
                    register[col_names[index]]=fields[index]
            if collection_name == 'PaperAbstractsInvertedIndex':
                inviabs = json.loads(register["IndexedAbstract"])
                abstract_text = self.inv_index2text(inviabs)
                register["Abstract"] = abstract_text
            return register
        else:
            pass

    def create_indexes(self,max_threads=None):
        indexes = []
        for collection_name in self.collection_names:
            col_indexes = MAColumnNames["nlp"]['{}_indexes'.format(collection_name)]
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
            if collection == "PaperAbstractsInvertedIndex":
                nlp_files = glob.glob(self.ma_dir+'nlp/PaperAbstractsInvertedIndex.txt.*')
                for nlp_file in nlp_files:
                    MAExecutor(self,nlp_file,"PaperAbstractsInvertedIndex",max_threads=max_threads)
            else:
                nlp_file=self.ma_dir+'nlp/{}.txt'.format(collection)
                MAExecutor(self,nlp_file,collection,max_threads=max_threads)
