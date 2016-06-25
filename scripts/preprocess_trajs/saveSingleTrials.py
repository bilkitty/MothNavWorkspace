#!/usr/bin/python3

"""
This script demonstrates how to save a set of trials from a one set of
conditions. The conditions are specified in a file named "conditions"
in the directory scripts. We expect the following format for "conditions":
   /scripts/conditions
   obstacle: <str_obstacle>
   moth_id: <str_moth_id>
   flight_speed: <float_flight_speed>
   fog_min: <float_fog_min>
   fog_max: <float_fog_max>
Once extracted, the set of trials are saved individually into a directory
path that is passed as the first argument to this script. If no path is
given, then no work is done and a usage error is uttered.
"""

import sys
import os.path as osp
from fileio import load_dataframe
from extractTrajs import get_trajs

def main():
   argc = len(sys.argv)
   if(argc == 2):
      path_to_data = sys.argv[1]
   else:
      print("(!) ERROR: Invalid args, see usage.\nUsage: ./saveTrials.py path_to_data")
      return
   # trim '/' off path
   end = len(path_to_data)-1
   if(path_to_data[end] == '/'):
      path_to_data = path_to_data[:end]

   print("Please specify the moth and trial conditions you want to save:")
   mid = input("'moth_id': ")
   obs = input("'obstacle': ")
   speed = float(input("'flight_speed': "))
   fmin = float(input("'fog_min': "))
   fmax = float(input("'fog_max': "))

   # read moth data
   dmoth = load_dataframe("h5","/media/usb/Input/moth_data.h5")

   # extract trials
   trajs = get_trajs(dmoth,obs,speed,fmin,fmax,mid)
   if(len(trajs) == 0):
      print("(!) ERROR: can't save trajs")
      return

   # save trials
   verbose_name = mid+'_'+str(int(speed))+str(int(fmin))+str(int(fmax))
   for ff in trajs:
      tt = dmoth[trajs[ff][0]:trajs[ff][1]]
      save_dataframe(tt,'h5',path_to_data+'/'+verbose_name+ff+".h5")
   return

if (__name__ == "__main__"):
   main()
