#!/usr/bin/python3

import pandas as pd
import os.path as osp

# returns NULL if failed to load file
def load_data(type,fpath):
   if(not osp.isfile(fpath)):
      print("(!) ERROR: "+fpath+" does not exist.")
      return None

   if(type == 'csv'):
      dt = pd.read_csv(fpath,delimiter=',')
   elif(type == 'h5'):
      # get name of data set by file name
      fname = fpath.split('/')[-1]
      dt = pd.read_hdf(fpath,fname.split('.')[0])
   else:
      print("(!) ERROR: file type, "+type+", is unrecognized.")
      dt = None

   return dt
