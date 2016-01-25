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
def print_sorted(d):
   sorted_by_val = sorted(d,key=d.get)
   last = len(sorted_by_val)-1

   print("{",end="")
   for k in sorted_by_val[:last]:
      print(' '+k+':'+str(d[k]))
   k = sorted_by_val[last]
   print(' '+k+':'+str(d[k])+"}")

   return

def count(items):
   d = {}
   for k in items:
      if(k in d.keys()):
         d[k] += 1
      else:
         d[k] = 1
   return d

# takes trial data frame
# returns a dicitonary:
# key = conditions, value = trial count
def count_trials(td):
   dd = count(td.obstacles)

   # check for reasonable siz
   if(len(dd) != 3):
      print("l(obst) = "+str(len(dd)))
   else:
      print("Obstacles:")
      print(dd)
      print_sorted(dd)


   # # flight_speed
   # dd = count(td.flight_speed)

   # # check for reasonable siz
   # if(len(dd) != 4):
   #    print("l(fs) = "+str(len(dd)))
   # else:
   #    print("Flight Speeds:")
   #    print(dd)


   # # fog_min
   # dd = count(td.fog_min)

   # # check for reasonable siz
   # if(len(dd) != 8):
   #    print("l(fmin) = "+str(len(dd)))
   # else:
   #    print("Fog Min:")
   #    print(dd)


   # # fog_max
   # dd = count(td.fog_max)

   # # check for reasonable size
   # if(len(dd) != 8):
   #    print("l(fmax) = "+str(len(dd)))
   # else:
   #    print("Fog Max:")
   #    print(dd)


   return

# returns NULL if failed to load file
def load_trials(path):
   dfile = path+'/trials.csv'
   if(osp.isfile(dfile)):
      dt = pd.read_csv(dfile)
   else:
      print("(!) ERROR: trials.csv does not exist in "+path)
      return None
   #--debug
   print(dt.iloc[0])
   return dt

# plot some data

def main():
   argc = len(sys.argv)
   if(argc == 2):
      path_to_data = sys.argv[1]
   else:
      print("(!) ERROR: Invalid args, see usage.\nUsage: ./loadYoyoData path_to_data")
      return

   # read trial data
   dtrial = load_trials(path_to_data)
   # if(not dtrial):
   #    return

   # count
   count_trials(dtrial)

   # read moth data
   # dmoth=pd.read_hdf(path_to_data+'/moth_data.h5','moth_data')


   print("~~Done :)")
   return

main()