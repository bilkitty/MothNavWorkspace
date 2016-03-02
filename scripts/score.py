#!/usr/bin/python3

from plotStuff import plot_frame
import numpy as np
import pandas as pd
import time

PAD = 0  # pad patch for discritization

def score_frame(mask,kernel):
   ret = 0 # elem wise mult and sum

   return ret

# ------ move to discretize.py --------#
# computes matrix indices as ith-block and
# jth-block between tcenter and origin.
def map_to_mat_idx(tcenter,orig,bsize):
  # use np arrays
  if(isinstance(orig,pd.Series)):
    origin = origin.values

  # get deltax, deltay of tree/moth
  tx2px = tcenter[0] - orig[0]
  ty2py = tcenter[1] - orig[1]
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
  # use np arrays
  if(isinstance(pt,pd.Series)):
    pt = pt.values
  if(isinstance(patch,pd.DataFrame)
    or isinstance(patch,pd.Series)):
    patch = patch.values

  print("discretizing")
  print("  patch origin: "+str(pt))
  print("  patch contains: "+str(len(patch)))
  print("  patch size: "+str(sz))

  if(rmin < 0):
    print("(!) Negative rmin")
    return None
  # get block size
  SZb = rmin/2
  print("  blocksize: "+str(SZb))

  # initialize matrix
  Nb = int(2*sz/SZb)
  # make sure matrix is oddxodd
  Nb += (Nb+1)%2
  # if(Nb > INTMAX)
  #   print("(!) Negative rmin")
  #   return None
  mat = np.zeros((Nb,Nb),dtype=int)

  # show moth block bm(0,0)
  mat[int(Nb/2)][int(Nb/2)] = -1

  cnt = 0 #debug
  for tt in patch:
     print("tree:"+str(cnt))
     # get tree center
     itt = map_to_mat_idx(tt,pt,SZb)
     Mi = int(Nb/2)+itt[0];
     Mj = int(Nb/2)+itt[1];

     # convert tree radius to nblocks
     rr =  tt[2]*2**.5
     rr /= 2
     rb = map_to_mat_idx((tt[0]+rr,tt[1]),tt,SZb)

     # create mask of ones over center+root(2)/2
     mask = (cnt+1)*np.ones((2*rb[0]+1,2*rb[0]+1),dtype=int)

     # set indices of mat[ti,tj] using mask
     xmin = Mi - rb[0]
     xmax = Mi + rb[0]
     ymin = Mj - rb[0]
     ymax = Mj + rb[0]

     # apply mask over tree center
     mat[xmin:xmax+1].T[ymin:ymax+1] = np.bitwise_or(mat[xmin:xmax+1].T[ymin:ymax+1],mask)

     # view error in reconstructing xy distance b/w tree and moth center
     print("  Mi="+str(Mi)+", Mj="+str(Mj))
     print("  tx="+str(tt[0])+"~ii*bsz+px="+str(itt[0]*SZb+pt[0]))
     print("  ty="+str(tt[1])+"~jj*bsz+px="+str(itt[1]*SZb+pt[1]))

     cnt += 1

  return [mat,SZb]
# ------ move to discretize.py --------#

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
