#!/usr/bin/python3

import sys
import os.path as osp
from loadYoyoData import load_data
from extractTrajs import get_trajs

DATA_FROM_USB = "/media/usb/Input/moth_data.h5"
MOTHS = ['moth7']#,'moth6','moth9']
# ,'moth1','moth2','moth8'
# ,'moth4','moth5','moth12'
# ,'moth10','moth3','moth11'
# ,'moth5_inc']

def saveMothTrials(dmoth,conditions,path_to_data):
   conditions.append('moth')
   print(conditions)
   for mid in MOTHS:
      # extract trials
      conditions[4] = mid
      trajs = get_trajs(dmoth,conditions)
      if(len(trajs) == 0):
         print("(!) ERROR: can't save trajs")
         return

      # save trials as mid_speed_fmin_fmax_trial.h5
      verbose_name = mid+'_'\
         +str(int(conditions[1]))\
         +str(int(conditions[2]))\
         +str(int(conditions[3]))
      for ff in trajs:
         tt = dmoth[trajs[ff][0]:trajs[ff][1]]
         if (not osp.exists(path_to_data+'/'+verbose_name+ff+".h5")):
            tt.to_hdf(path_to_data+'/'+verbose_name+ff+".h5",
               verbose_name+ff,
               format='table',
               mode='w')

   return

def main():
   path_to_data = ""
   conditions = []

   argc = len(sys.argv)
   if(argc != 3):
      print("(!) ERROR: Insufficient args.\nUsage: .py path_to_data conditions_spec")
      return

   # verify arguments
   if osp.exists(sys.argv[1]):
      path_to_data = sys.argv[1]
   else:
      print("(!) ERROR: path to data does not exist")
      return

   ilines = []
   if osp.exists(sys.argv[2]):
      ff = open(sys.argv[2])
      ilines = [line.strip('\n') for line in ff.readlines()]

   # trim '/' off path
   end = len(path_to_data)-1
   if(path_to_data[end] == '/'):
      path_to_data = path_to_data[:end]
   print(" Writing files to: "+path_to_data)

   # parse conditions
   for line in ilines:
      if not ':' in line:
         continue

      cc = line.replace(' ','').split(":")
      val = cc[1]

      if (cc[0] == 'obstacle'):
         conditions.append(val)
      elif (cc[0] == 'speed'):
         conditions.append(float(val))
      elif (cc[0] == 'fog_min'):
         conditions.append(float(val))
      elif (cc[0] == 'fog_max'):
         if (len(conditions) == 3 and float(val) <= conditions[2]):
            print("(!) fmax <= fmin")
            continue
         conditions.append(float(val))
      else:
         print("(!) Condition "+str(cc)+" is invalid")

   if (len(conditions) < 4):
      print("(!) ERROR: Insufficient conditions")
      return

   # read moth data
   dmoth = load_data("h5",DATA_FROM_USB)

   # generate and save trials for condition set
   saveMothTrials(dmoth,conditions,path_to_data)

   return



main()
