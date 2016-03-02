#!/usr/bin/python3

from loadYoyoData import load_data
from plotStuff import plot_frame, plot_mat
from score import setup_test, discretize

def main():
   # read moth and tree data
   dtree = load_data("csv","../data/test/forest.csv")
   dmoth = load_data("csv","../data/test/moth6_single.csv")    # check for loaded files

   # check that moth and tree data are not empty
   if(len(dtree)+len(dmoth) == 0):
      printf("(!) ERROR: No data loaded.")
      return

   # setup test data
   [pt,patch,sz] = setup_test(dmoth,dtree)

   # get discretrized matrix
   [mat,bsize] = discretize(pt,patch,sz,min(dtree.r)/2)

   # plot_frame(pt,patch,sz,dtree,"../data/test/moth6_frame.png")
   # plot_mat(mat,bsize,"../data/test/moth6_kernel.png")

   plot_frame(pt,patch,sz,dtree)#,"moth6_frame.png")
   plot_mat(mat,bsize)#,"moth6_kernel.png")


   print("~~Done :)")
   return

main()