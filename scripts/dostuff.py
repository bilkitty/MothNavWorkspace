#!/usr/bin/python3

import sys
from loadYoyoData import load_data
from extractTrajs import get_trajs
from plotTrials import plot
from collisions import count_collisions_closecalls

weird_moth = 'moth5_inc'

def main():
   argc = len(sys.argv)
   if(argc == 3):
      path_to_data = sys.argv[1]
      plot_output = sys.argv[2]
   else:
      print("(!) ERROR: Invalid args, see usage.\nUsage: ./plot_moth_data path_to_data output.png")
      return
   # trim '/' off path
   end = len(path_to_data)-1
   if(path_to_data[end] == '/'):
      path_to_data = path_to_data[:end]

   # read moth and tree data
   dtree = load_data("csv","/media/usb/Input/forest.csv")
   dmoth = load_data("h5","../data/single_trials/moth1_448f0.h5")    # check for loaded files
   # if(not dtrial):
   #    return

   # check that tt is not empty
   # check that tree is not emtpy
   # plot(tt,dtree,plot_output)

   # detect collisions
   count_collisions_closecalls(dmoth,dtree)

   print("~~Done :)")
   return

main()