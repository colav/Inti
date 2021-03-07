

from inti.MA.MAMag import MAMag
from inti.MA.MANlp import MANlp

from pymongo import MongoClient
import psutil
import logging
import sys

class MALoader:
    def __init__(self,ma_dir,database_name,sep='\t', buffer_size=1024*10, dburi='mongodb://localhost:27017/',
                 log_file='mamagloader.log', info_level=logging.DEBUG):
        """
        Class to load the different files from MA directories,

        by default the method run, execute the code to load all the files,
        you can to specify the file, given the argument to the methdo run, lets see run documentation for more details.
        """
        self.ma_dir = ma_dir
        self.database_name = database_name
        self.sep = sep
        self.buffer_size = buffer_size
        self.dburi = dburi
        self.log_file = log_file
        self.info_level = info_level
    
    def run(self,sub_folder,max_threads=None):
        """
        Subfolder can be mag,nlp or advanced
        """
        if sub_folder not in ["mag","nlp"]:
            print("Error: sub_folder should be mag or nlp")
            sys.exit(1) 
        if sub_folder == "mag":
            mag = MAMag(self.ma_dir,self.database_name,self.sep,self.buffer_size,self.dburi,self.log_file,self.info_level)
            mag.run(max_threads)
        if sub_folder == "nlp":
            mag = MANlp(self.ma_dir,self.database_name,self.sep,self.buffer_size,self.dburi,self.log_file,self.info_level)
            mag.run(max_threads)        