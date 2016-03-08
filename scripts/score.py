#!/usr/bin/python3

from plotStuff import plot_frame, plot_mat
from discretize import discretize
import numpy as np
import pandas as pd
import sys

PAD = 10  # pad patch for discritization

def is_square_mat(mat):
   if(mat.shape[0] == 0 or mat.shape[1] == 0):
      print("(!) Mat is flat or empty")
      return False

   return mat.shape[0] == mat.shape[1]

def score_frame(mask,kernel):
   ret = 0 # elem wise mult and sum
   if(is_square_mat(mask) and is_square_mat(kernel)):
     prod = np.multiply(mask,kernel)
     ret = prod.sum()
   # is this meaningful?
   # represent score as percent coverage if kernel is uniform ones
   ret = 1 - ret/mask.shape[0]/mask.shape[1]
   return ret

# generates data frame slice of env objects
# contained within a square around origin.
# ARGS: origin (to center patch on), forest
# RETURNS: tree patch, patch size (L/2 of
# patch, not number of trees)
def get_patch(orig,env,partial=True):
   patch_size = (int)(50*max(env.r)/2) + PAD # floored
   if(not partial):
     l = orig[0]-patch_size < env.x-env.r
     r = env.x+env.r < orig[0]+patch_size
     u = env.y+env.r < orig[1]+patch_size
     d = orig[1]-patch_size < env.y-env.r
   else:
     l = orig[0]-patch_size < env.x+env.r
     r = env.x-env.r < orig[0]+patch_size
     u = env.y-env.r < orig[1]+patch_size
     d = orig[1]-patch_size < env.y+env.r
   patch = env[l & r & u & d]
   return [patch, patch_size]

# generate a kernel whose
def generateKernel(ktype,size):
   ret = np.ones((size,size),dtype=int)
   # create vertical split
   if(ktype == 'vertical split'):
      split_size = int(ret.shape[0] / 10)
      ret[(ret.shape[0]/2)-split_size:(ret.shape[0]/2)+split_size+1] = -1
      ret = ret.T

   # otherwise return uniform
   return ret

# think about keeping data frames as is for simplicity
def walk(dm, td, ktype='uniform', display=False):
   cummulative_score = 0
   min_score = sys.maxsize
   max_score = -sys.maxsize - 1
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

   cnt = 1
   # get mask of first point
   [patch,sz] = get_patch(dm.loc[0],td)

   [mask, bsize] = discretize(dm.loc[0],patch,sz,min(td.r))
   # initialize kernel
   kernel = generateKernel(ktype,mask.shape[0])
   # initialize score
   if(is_square_mat(mask) and is_square_mat(kernel)):
      score = score_frame(mask,kernel)
      if(score < min_score): min_score = score
      if(max_score < score): max_score = score
      cummulative_score += score
   else:
      print("(!) Walk: Either mask or kernel is not square")

   if(display):
      plot_mat(mask,bsize,"initial_mask.png")

   # process other points
   for point in dm.values[1:10]:
      cnt += 1
      print("pt "+str(cnt)+" ("+str(round(point[0],3))+","+str(round(point[1],3))+"):",end='')
      # get scoring region, may contain trees
      [patch,sz] = get_patch(point,td)
      print("\t"+str(len(patch.values))+" ts")
      # discretize that shit
      [mask, bsize] = discretize(point,patch,sz,min(td.r))

      # update score
      if(is_square_mat(mask) and is_square_mat(kernel)):
         score = score_frame(mask,kernel)
         if(score < min_score): min_score = score
         if(max_score < score): max_score = score
         cummulative_score += score
      else:
         print("(!) Either mask or kernel is not square")

      if(display):
         plot_mat(mask,bsize,"./masks/mask"+str(cnt)+".png")


   print("===== SCORE =====")
   print("cummulative_score: "+str(cummulative_score))
   print("min_score: "+str(min_score))
   print("max_score: "+str(max_score))

   return 0