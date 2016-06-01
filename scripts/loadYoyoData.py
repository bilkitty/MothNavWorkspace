#!/usr/bin/python3

import pandas as pd
import os.path as osp
import time

# consider data -> dataframe to be more specific

# returns NULL if failed to load file
def load_data(type,file_path):
   if(not osp.isfile(file_path)):
      print("(!) ERROR: "+file_path+" does not exist.")
      return None

   print("loading: "+file_path)
   start = time.time() # sec

   if(type == 'csv'):
      dt = pd.read_csv(file_path,delimiter=',')
   elif(type == 'h5'):
      # get name of data set by file name
      fname = file_path.split('/')[-1]
      dt = pd.read_hdf(file_path,fname.split('.')[0])
   else:
      print("(!) load_data: file type, "+type+", is unrecognized.")
      dt = None

   # print("  PT(ms): "+ str(round(1000*(time.time() - start),5)))

   return dt

def save_data(data_frame,type,file_path):
   """
   (str,str,pandas.dataframe) -> None
   Save data_frame as cvs or hdf in the given file path.
   """
   if (type == 'csv'):
      data_frame.to_csv(file_path)
   else:
      print("(!) save_data: file type, "+type+", is unrecognized.")

   return