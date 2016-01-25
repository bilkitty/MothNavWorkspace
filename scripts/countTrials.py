#!/usr/bin/python3

import pandas as pd
import os.path as osp
import sys

def print_sorted(d):
   sorted_by_val = sorted(d,key=lambda x:d[x],reverse=True)
   last = len(sorted_by_val)-1

   k = sorted_by_val[0]
   print(' '+str(k)+'='+str(d[k]))
   for k in sorted_by_val[1:]:
      print(','+str(k)+'='+str(d[k]))
   print()

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
   # moth count
   dd = count(td.moth_id)
   print("MothIds:")
   print_sorted(dd)

   # obstacles
   dd = count(td.obstacles)
   print("Obstacles:")
   print_sorted(dd)

   # flight_speed
   dd = count(td.flight_speed)
   print("Flight Speeds:")
   print_sorted(dd)

   # fog_min
   dd = count(td.fog_min)
   print("Fog Min:")
   print_sorted(dd)

   # fog_max
   dd = count(td.fog_max)
   print("Fog Max:")
   print_sorted(dd)

   return

# returns NULL if failed to load file
def load_trials(path):
   dfile = path+'/trials.csv'
   if(osp.isfile(dfile)):
      dt = pd.read_csv(dfile)
   else:
      print("(!) ERROR: trials.csv does not exist in "+path)
      return None

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

   print("~~Done :)")
   return

main()