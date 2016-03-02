#!/usr/bin/python3

from loadYoyoData import load_data
import walkTraj
import time

def main():
   start = time.time()
   # read moth and tree data
   dtree = load_data("csv","../data/test/forest.csv")
   dmoth = load_data("csv","../data/test/moth6_single.csv")    # check for loaded files

   # check that moth and tree data are not empty
   if(len(dtree)+len(dmoth) == 0):
      printf("(!) ERROR: No data loaded.")
      return

   walkTraj.walk(dmoth,dtree,display=True)
   print("Total CPU Time: "+str(round(time.time() - start,5)))
   print("~~Done :)")
   return

main()