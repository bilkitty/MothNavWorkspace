#!/usr/bin/python3

import sys
import os.path as osp
from loadYoyoData import load_data
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
   speed = float(input("'speed': "))
   fmin = float(input("'fog_min': "))
   fmax = float(input("'fog_max': "))

   # read moth data
   dmoth = load_data("h5","/media/usb/Input/moth_data.h5")

   # extract trials
   trajs = get_trajs(dmoth,obs,speed,fmin,fmax,mid)
   if(len(trajs) == 0):
      print("(!) ERROR: can't save trajs")
      return

   # save trials
   verbose_name = mid+'_'+str(int(speed))+str(int(fmin))+str(int(fmax))
   for ff in trajs:
      tt = dmoth[trajs[ff][0]:trajs[ff][1]]
      tt.to_hdf(path_to_data+'/'+verbose_name+ff+".h5",
         verbose_name+ff,
         format='table',
         mode='w')


   return



main()

