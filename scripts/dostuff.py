#!/usr/bin/python3

import sys
from loadYoyoData import load_data
from extractTrajs import get_trajs
from plotTrials import plot

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
   dtree = load_data("csv","/media/usb/data_working/forest_sans_header.csv") # 12 labels (no obst)
   dmoth = load_data("h5","/media/usb/Input/moth_data.h5") # 13 labels
   # check for loaded files
   # if(not dtrial):
   #    return

   # test plot all of moth_n
   trajs = get_trajs(dmoth,'bright',4.0,4.0,8.0,weird_moth)
   tt = dmoth[trajs['f0'][0]:trajs['f0'][1]]

   # check that tt is not empty
   # check that tree is not emtpy
   plot(tt,dtree,plot_output)

   print("~~Done :)")
   return

main()