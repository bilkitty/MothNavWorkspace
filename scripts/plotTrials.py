#!/usr/bin/python3

import pandas as pd   # data handling
import numpy as np    # plotting
import os.path as osp # file exists
import sys            # commandline args

weird_moth = 'moth5_inc'
DEBUG = True

def plot(traj,env):
   # (0) check that traj is 2 dims, otherwise can't plot

   # (2) plot moth points
   print("plottig pts: "+str(len(traj)))

   # (1) plot trees alone
   print("plottig trees: "+str(len(env)))



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
   dtree = load_data('csv',path_to_data+'/bright_trees.csv') # 12 labels (no obst)
   dmoth = load_data('h5',path_to_data+'/moth_data.h5') # 13 labels
   # check for loaded files
   # if(not dtrial):
   #    return

   # select moth candidate
   moths = [0]*13
   for nn in range(1,13):
      moths[nn-1] = dmoth.loc[dmoth['moth_id'] == 'moth'+str(nn)]
   moths[len(moths)-1] = dmoth.loc[dmoth['moth_id'] == weird_moth]

   #-- check that split was done correctly
   if(DEBUG):
      moth_trial_count = [0]*13
      nn = 0
      for mm in moths:
         moth_trial_count[nn] = len(mm)
         nn += 1
      if(not (sum(moth_trial_count) == len(dmoth))):
         print("(!) moth trials don't add up to total trials")
      else:
         print("Trial count per moth:")
         print(moth_trial_count)

   m1 = moths[0].loc[moths[0].flight_speed == 2.0]
   tree = dtree[0].loc[dtree[0].flight_speed == 2.0] # check that moth and datetime match
   plot(m1,tree)










   print("~~Done :)")
   return

main()