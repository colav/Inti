#!/usr/bin/env python3
from inti.MA.MAMagLoader import MAMagLoader

import argparse
import logging

parser = argparse.ArgumentParser(description='Process papers with GSLookUp.')
parser.add_argument('--max_threads', type=int,default=None, help='an integer for number of threads')
parser.add_argument('--db',required=True, type=str, help='database name to read the data collection (ex: udea,redalyc)')
parser.add_argument('--mag_dir',required=True, type=str, help='MAG directory with the txt files wiht the data (ex: /storage/MA/mag)')
parser.add_argument('--debug', action='store_true', help='Produces a lot of output messages for debug')
parser.add_argument('--create_indexes', action='store_true', help='Create Indexes for all the collections')
parser.add_argument('--db_ip', type=str, default='localhost',
                    help='mongodb ip (default localhost)')
parser.add_argument('--db_port', type=int, default=27017,
                    help='mongodb port (default 27017)')

args = parser.parse_args()

level=logging.INFO
if args.debug:
    level=logging.DEBUG

dburi='mongodb://{}:{}/'.format(args.db_ip,args.db_port)

loader=MAMagLoader(mag_dir=args.mag_dir,database_name=args.db,dburi=dburi,info_level=level)


logging.warning("--------------------------------------------------------\n")
logging.warning("Starting MA MAG Loader ")
if args.create_indexes:
    loader.create_indexes(max_threads=args.max_threads)
else:
    loader.run(max_threads=args.max_threads)
logging.warning("MA MAG Loader finished! ")
logging.warning("--------------------------------------------------------\n")
