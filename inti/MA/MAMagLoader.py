

from inti.MA.MAMagBase import MAMagBase, MAMagColNames
import logging

class MAMagLoader:
    def __init__(self,mag_dir,database_name,sep='\t', buffer_size=1024*1024, dburi='mongodb://localhost:27017/', hunabku_server = None, hunabku_apikey = None,
                 log_file='mamagloader.log', info_level=logging.DEBUG):
        """
        Class to load the different files from mag directory,
        the directory should have the next files
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

        by default the method run, execute the code to load all the files,
        you can to specify the file, given the argument to the methdo run, lets see run documentation for more details.
        """
        self.collections = ['Authors']#,'Affiliations','PaperAuthorAffiliations','Papers','PaperUrls','PaperResources','PaperReferences','PaperExtendedAttributes','Journals','ConferenceSeries','ConferenceInstances']
        self.mag_dir = mag_dir
        self.database_name = database_name
        self.sep = sep
        self.buffer_size = buffer_size
        self.dburi = dburi
        self.hunabku_server = hunabku_server
        self.hunabku_apikey = hunabku_apikey
        self.log_file = log_file
        self.info_level = info_level
        

    def run(self,max_threads=None,instace=None):
        for collection in self.collections:
            mag_file=self.mag_dir+'/{}.txt'.format(collection)
            col_names = MAMagColNames[collection]
            col_indexes = MAMagColNames['{}_indexes'.format(collection)]

            instance = MAMagBase(mag_file,self.database_name,collection,col_names,col_indexes,self.sep, self.buffer_size, self.dburi, self.hunabku_server, self.hunabku_apikey,self.log_file, self.info_level)
            instance.run(max_threads=max_threads)
         