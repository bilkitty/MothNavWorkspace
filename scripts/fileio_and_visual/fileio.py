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
  >>> filepath = os.getcwd()+"/test/test.h5"
  >>> fileformat = "h5"
  >>> datah5 = load_dataframe(fileformat,filepath)
  loading: /home/bilkit/Dropbox/moth_nav_analysis/scripts/test/test.h5
  >>> datah5.shape
  (1000, 3)
  >>> datacsv = load_dataframe("csv","/home/bilkit/Dropbox/moth_nav_analysis/scripts/test/test.csv")
  loading: /home/bilkit/Dropbox/moth_nav_analysis/scripts/test/test.csv
  >>> datacsv.shape
  (1000, 3)
  """
  if(not os.path.isfile(file_path)):
    raise FileNotFoundError("(!) ERROR: {:s} does not exist.".format(file_path))

  print("loading: "+file_path)
  dt = None
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


  return dt

def save_dataframe(data_frame,file_format,file_path):
  """
  (pandas.dataframe,str,str) -> None

  Save a data frame according to file format (cvs or hdf) at the
  given file path. The data is saved without an index. If file
  path doesn't exist then an exception is thrown.

  >>> datacsv = load_dataframe("csv","/home/bilkit/Dropbox/moth_nav_analysis/scripts/test/trees.csv")
  loading: /home/bilkit/Dropbox/moth_nav_analysis/scripts/test/trees.csv
  >>> save_dataframe(datacsv,"csv",os.getcwd()+"/test/test.csv")
  >>> save_dataframe(datacsv,"h5",os.getcwd()+"/test/test.h5")
  """
  filename = file_path.split('/')[-1]
  file_location = file_path.replace(filename,"")
  if (not os.path.exists(file_location)):
    raise NotADirectoryError("(!) ERROR: {:s} does not exist.".format(file_location))

  if (file_format == 'csv'):
    try:
      data_frame.to_csv(file_path,index=False)
    except OSError:
      print("(!) You passed a directory path instead of a file path.")
  elif (file_format == 'h5'):
    filename = file_path.split('/')[-1]
    # replace default key with filename
    key = "data"
    if (filename.split('.')[0] != filename):
      key = filename.split('.')[0]
    else:
      print("(!) Saving {:s} with key={:s}".format(file_path,key))
    try:
      data_frame.to_hdf(file_path,key=key)
    except OSError:
      print("(!) You passed a directory path instead of a file path.")
  else:
    print("(!) save_data: file file_format, "+file_format+", is unrecognized.")

  return

""" DOC TESTS """
if __name__ == "__main__":
  import doctest
  doctest.testmod()