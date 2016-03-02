#!/usr/bin/python3

import pandas as pd
import numpy as np
from score import get_patch \
                  ,discretize \
                  ,score_frame
from plotStuff import plot_mat
import time

# generate score for single traj point

# args:
# traj data
# tree data

# return:
# n/a

# steps:
# loop though traj points
# slice tree patch floor edges
# pass that ish to score
# record result as text and in plot
# save plot and text

# generate a kernel whose
def generateKernel(ktype,size):
   ret = np.ones((size,size),dtype=int)
   # create vertical split
   if(ktype == 'vertical split'):
      ret[ret.shape[0]/2] = -1
      ret = ret.T

   # otherwise return uniform
   return ret

def is_square_mat(mat):
   if(mat.shape[0] == 0 or mat.shape[1] == 0):
      print("(!) Mat is flat or empty")
      return False

   return mat.shape[0] == mat.shape[1]


# think about keeping data frames as is for simplicity
def walk(dm, td, ktype='uniform', display=False):
   cummulative_score = 0
   # get moth xy data from data frame
   dm = dm[['pos_x','pos_y']]
   # make sure there are data in moth data frame
   if(len(dm.values) == 0 or len(dm.values[0]) != 2):
      print("(!) Cannot process traj data of size:"+str(len(dm.values))\
         +" & len:"+str(len(dm.values[0])))
      return 1
   if(len(td.values) == 0 or len(td.values[0]) != 3):
      print("(!) Cannot process tree data of size:"+str(len(td.values))\
         +" & len:"+str(len(td.values[0])))
      return 1

   # measure processing times
   # 0 = get_patch, 1 = discritize
   procTime = [0.,0.]
   # get mask of first point
   start = time.time()
   [patch,sz] = get_patch(dm.loc[0],td)
   procTime[0] += time.time() - start

   start = time.time()
   [mask, bsize] = discretize(dm.loc[0],patch,sz,min(td.r))
   procTime[1] += time.time() - start
   # initialize kernel
   kernel = generateKernel(ktype,mask.shape[0])
   # initialize score
   if(is_square_mat(mask) and is_square_mat(kernel)):
      cummulative_score += score_frame(mask,kernel)
   else:
      print("(!) Either mask or kernel is not square")

   if(display):
      plot_mat(mask,bsize,"initial_mask.png")

   cnt = 1
   # process other points
   for point in dm.values[1:5]:
      # get scoring region, may contain trees
      start = time.time()
      [patch,sz] = get_patch(point,td)
      procTime[0] += time.time() - start

      # discretize that shit
      start = time.time()
      [mask, bsize] = discretize(point,patch,sz,min(td.r))
      procTime[1] += time.time() - start

      # update score
      if(is_square_mat(mask) and is_square_mat(kernel)):
         cummulative_score += score_frame(mask,kernel)
      else:
         print("(!) Either mask or kernel is not square")

      if(display):
         plot_mat(mask,bsize,"mask"+str(cnt)+".png")

      cnt += 1

   print("cummulative_score: "+str(cummulative_score))
   print("get_patch avg PT(ms): "+str(round(procTime[0]/cnt,5)))
   print("discretize avg PT(ms): "+str(round(procTime[1]/cnt,5)))


   return 0