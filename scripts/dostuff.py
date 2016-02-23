#!/usr/bin/python3

import sys
from loadYoyoData import load_data
from extractTrajs import get_trajs
from plotTrials import plot
from collisions import count_collisions_closecalls
from score import setup_test

weird_moth = 'moth5_inc'

def main():
   argc = len(sys.argv)
   # read moth and tree data
   dtree = load_data("csv","../data/test/forest.csv")
   dmoth = load_data("csv","../data/test/moth6_single.csv")    # check for loaded files

   # check that moth and tree data are not empty
   if(len(dtree)+len(dmoth) == 0):
      printf("(!) ERROR: No data loaded.")
      return

   # setup test data
   setup_test(dmoth,dtree)

   print("~~Done :)")
   return

main()