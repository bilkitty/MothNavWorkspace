#!/usr/bin/python3

import pandas as pd
import os.path as osp

# consider data -> dataframe to be more specific

# returns NULL if failed to load file
def load_dataframe(type,file_path):
   if(not osp.isfile(file_path)):
      print("(!) ERROR: "+file_path+" does not exist.")
      return None

   print("loading: "+file_path)

   if(type == 'csv'):
      dt = pd.read_csv(file_path,delimiter=',')
   elif(type == 'h5'):
      # get name of data set by file name
      fname = file_path.split('/')[-1]
      dt = pd.read_hdf(file_path,fname.split('.')[0])
   else:
      print("(!) load_data: file type, "+type+", is unrecognized.")
      dt = None


   return dt

def save_dataframe(data_frame,type,file_path):
   """
   (str,str,pandas.dataframe) -> None
   Save data_frame as cvs or hdf in the given file path.
   """
   if (type == 'csv'):
      data_frame.to_csv(file_path,index=False)
   else:
      print("(!) save_data: file type, "+type+", is unrecognized.")

   return