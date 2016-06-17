#!/usr/bin/python3

import pandas as pd
import os

def load_dataframe(file_format,file_path):
   """
   (str,str) -> pandas.dataframe

   Given a file_format (i.e., csv or h5) and path, attempt
   to load and return a data frame. If file path doesn't exist
   or file file_format is not csv or h5, then return None.

   Examples:
   >>> filepath = "/home/bilkit/Dropbox/moth_nav_analysis/data/single_trials/moth1_448f0.h5"
   >>> fileformat = "h5"
   >>> datah5 = load_dataframe(fileformat,filepath)
   loading: /home/bilkit/Dropbox/moth_nav_analysis/data/single_trials/moth1_448f0.h5
   >>> datah5.shape
   (3454, 13)
   >>> datacsv = load_dataframe("csv","/home/bilkit/Dropbox/moth_nav_analysis/data/forests/forest.csv")
   loading: /home/bilkit/Dropbox/moth_nav_analysis/data/forests/forest.csv
   >>> datacsv.shape
   (1000, 3)
   """
   if(not os.path.isfile(file_path)):
      print("(!) ERROR: "+file_path+" does not exist.")
      return None

   print("loading: "+file_path)

   if(file_format == 'csv'):
      dt = pd.read_csv(file_path,delimiter=',')
   elif(file_format == 'h5'):
      # use filename (sans extention) as key
      filename = file_path.split('/')[-1]
      key = filename.split('.')[0]
      try:
         dt = pd.read_hdf(file_path,key)
      except KeyError:
         print("Key {:s} doesn't exist, so can't load data from {:s}.".format(key,file_path))

   else:
      print("(!) load_data: file file_format, "+file_format+", is unrecognized.")
      dt = None


   return dt

def save_dataframe(data_frame,file_format,file_path):
   """
   (pandas.dataframe,str,str) -> None

   Save a data frame according to file format (cvs or hdf) at the
   given file path. The data is saved without an index. If file
   path doesn't exist then an exception is thrown.

   >>> datacsv = load_dataframe("csv","/home/bilkit/Dropbox/moth_nav_analysis/data/forests/forest.csv")
   loading: /home/bilkit/Dropbox/moth_nav_analysis/data/forests/forest.csv
   >>> save_dataframe(datacsv,"csv",os.getcwd()+"/test.csv")
   >>> save_dataframe(datacsv,"h5",os.getcwd()+"/test.h5")
   """
   filename = file_path.split('/')[-1]
   file_location = file_path.replace(filename,"")
   if (not os.path.exists(file_location)):
      raise EXCEPTION("Filepath doesn't exist")

   if (file_format == 'csv'):
      data_frame.to_csv(file_path,index=False)
   elif (file_format == 'h5'):
      filename = file_path.split('/')[-1]
      # replace default key with filename
      key = "data"
      if (filename.split('.')[0] != filename):
         key = filename.split('.')[0]
      else:
         print("(!) Saving {:s} with key={:s}".format(file_path,key))
      data_frame.to_hdf(file_path,key=key)
   else:
      print("(!) save_data: file file_format, "+file_format+", is unrecognized.")

   return

""" DOC TESTS """
if __name__ == "__main__":
   import doctest
   doctest.testmod()