#!/usr/bin/python3

import pandas as pd
import numpy as np
from score import get_patch \
                  ,discretize \
                  ,score_frame

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
KERNELS = ['uniform','vslit','gaussian']

# generate a kernel whose
def generateKernel(ntype,size):
   ret = np.ones((size,size),dtype=int)
   # create vertical split
   if(ntype == 2):
      ret[ret.shape[0]/2] = -1
      ret = ret.T

   # otherwise return uniform
   return ret

# think about keeping data frames as is for simplicity
def walk(dm, td, nkern=0, display=False):
   # get moth xy data from data frame
   # if(isinstance(dm,pd.DataFrame) or isinstance(dm,pd.Series)):
   #    dm = dm[['pos_x','pos_y']].values
   # if(isinstance(td,pd.DataFrame) or isinstance(td,pd.Series)):
   #    td = td.values
   dm = dm[['pos_x','pos_y']]
   # make sure there are data in moth data frame
   if(len(dm.values) == 0 or len(dm.values[0]) != 2):
      print("(!) Cannot process traj data of size:"+str(len(dm.values))\
         +" & len:"+str(len(dm.values[0])))
      return 1
   if(len(td.values) == 0 or len(td.values) != 3):
      print("(!) Cannot process tree data of size:"+str(len(td.values))\
         +" & len:"+str(len(td.values[0])))
      return 1

   # get mask of first point
   [patch,sz] = get_patch(dm.loc[0],td)
   [mask, bsize] = discretize(dm.loc[0],patch,sz,min(td.r))
   # initialize kernel
   kernel = generateKernel(nkern,mask.shape[0])
   # initialize score
   cummulative_score = score_frame(mask,kernel)

   # # process other points
   # for point in dm.values[1:5]:
   #    # get scoring region, may contain trees
   #    [patch,sz] = get_patch(point,td)
   #    # if(display):
   #    #    plot_frame(xypoint,patch,patch_size,td)

   #    # discretize that shit
   #    [mask, bsize] = discretize(point,patch,sz,min(td[:].T[2]))

      # cummulative_score += score_frame(mask,kernel)





   return 0