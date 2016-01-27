#!/usr/bin/python3

import pandas as pd
import os.path as osp
import sys

weird_moth = 'moth5_inc'

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

# plot some data

def main():
   argc = len(sys.argv)
   if(argc == 2):
      path_to_data = sys.argv[1]
   else:
      print("(!) ERROR: Invalid args, see usage.\nUsage: ./plot_moth_data path_to_data")
      return
   # trim '/' off path
   end = len(path_to_data)-1
   if(path_to_data[end] == '/'):
      path_to_data = path_to_data[:end]

   # read moth and tree data
   dtree = load_data('csv',path_to_data+'/dark_trees.csv') # 12 labels (no obst)
   dmoth = load_data('h5',path_to_data+'/moth_data.h5') # 13 labels
   # check for loaded files
   # if(not dtrial):
   #    return

   print("~~Done :)")
   return

main()