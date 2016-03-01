#!/usr/bin/python3

from plotTrials import plot_frame
from math import floor
import numpy as np
import pandas as pd

PAD = 0  # pad patch for discritization

def score(pt,patch,size,rmin):
   ret = 0 # convolution result

   return ret

# computes matrix indices as ith-block and
# jth-block between tcenter and origin.
def map_to_mat_idx(tcenter,orig,bsize):
   # get deltax, deltay of tree/moth
   tx2px = tcenter[0] - orig.pos_x
   ty2py = tcenter[1] - orig.pos_y
   # get half blocks between mcenter and tcenter
   ihalf = int( 2*tx2px/bsize ) # cols are x
   jhalf = int( 2*ty2py/bsize ) # rows are y
   # convert to index by combining halves
   ii = ihalf if abs(ihalf) < 2 else int(ihalf/2)
   jj = jhalf if abs(jhalf) < 2 else int(jhalf/2)

   return (ii,jj)

# divide patch into min tree radius/2 sized
# blocks and bin tree points into a matrix
# MxM.
# ARGS: moth point, tree patch, patch size,
#   min(tree radius)
# RETURNS: matrix MxM, block size, where
#   M = 2*patch/block size (odd)
def discretize(pt,patch,sz,rmin):
  print("discretizing")
  if(not isinstance(patch,pd.DataFrame)):
     print("  (!) patch is not data frame")
     return None
  print("  patch contains: "+str(len(patch)))
  print("  patch size: "+str(sz))

  # get block size
  SZb = rmin/2
  print("  blocksize: "+str(SZb))

  # initialize matrix
  Nb = int(2*sz/SZb)
  # make sure matrix is oddxodd
  Nb += (Nb+1)%2
  mat = np.zeros((Nb,Nb))

  # show moth block bm(0,0)
  mat[Nb/2][Nb/2] = -1

  cnt = 0 #debug
  for tt in patch.values:
     print("tree:"+str(cnt))
     itt = map_to_mat_idx(tt,pt,SZb)

     Mi = (Nb/2)+itt[0];
     Mj = (Nb/2)+itt[1];

     # view error in reconstructing xy distance b/w tree and moth center
     print("  ii="+str(itt[0])+", jj="+str(itt[1]))
     print("  tx="+str(tt[0])+"~ii*bsz+px="+str(itt[0]*SZb+pt.pos_x))
     print("  ty="+str(tt[1])+"~jj*bsz+px="+str(itt[1]*SZb+pt.pos_y))

     # indicate tree center in matrix index
     mat[Mi][Mj] = cnt+1 # show which tree is where
     # mat[(Nb/2)+Bi][(Nb/2)+Bj] = 1

     cnt += 1

  return [mat,SZb]

# generates data frame slice of env objects
# contained within a square around origin.
# ARGS: origin (to center patch on), forest
# RETURNS: tree patch, patch size (radius not
#   number of trees)
def get_patch(orig,env):
   patch_size = (int)(50*max(env.r)/2) + PAD
   l = orig[0]-patch_size < env.x+env.r
   r = env.x-env.r < orig[0]+patch_size
   u = env.y-env.r < orig[1]+patch_size
   d = orig[1]-patch_size < env.y+env.r
   patch = env[l & r & u & d]
   return [patch, patch_size]

# sets up tree patch centered on single point
# from moth traj and tree data.
# Also provides visualization of patch by default.
# ARGS: moth_traj, tree_data, bool (opt)
# RETURNS: moth_point, tree_patch, patch_size(L/2)
def setup_test(md,td,display=False):
   # get a single point
   xypoint = md.loc[0] #(int)((len(md)-1)/2)] # midpoint
   xy = xypoint[['pos_x','pos_y']]
   print("centering around point: ("+str(xy.pos_x)+","+str(xy.pos_y)+")")

   # get patch centered on moth point
   # size is L/2 for patch LxL
   [patch,patch_size] = get_patch(xy,td)

   # visualize patch
   if(display):
      plot_frame(xypoint,patch,patch_size,td)

   return [xy,patch,patch_size]
