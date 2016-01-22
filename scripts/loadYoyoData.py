#!/usr/bin/python3

import pandas as pd
import os.path as osp
import sys

# count trials
   # count conditions used for all trials
   # blue
   # bright
   # dark
   # speed 1,2,4,8
   # fmin (8 of these)
   # fmax (8 of those)


# plot some data

def main():
   argc = len(sys.argv)
   if(argc == 2):
      path_to_data = sys.argv[1]
   else:
      print("(!) ERROR: Invalid args, see usage.\nUsage: ./loadYoyoData path_to_data\n")
      return

   # read trial data
   dfile = path_to_data+'/trials.csv'
   if(osp.isfile(dfile)):
      dtrial = pd.read_csv(dfile)
   else:
      print("(!) ERROR: trials.csv does not exitst in "+path_to_data+"\n")
      return
   # analyse trial data
   print(dtrial.iloc[0])

   # read moth data
   # dmoth=pd.read_hdf(path_to_data+'/moth_data.h5','moth_data')


   print("~~Done :)")
   return

main()