#!/usr/bin/python3

from plotTrials import plot_frame
from math import floor
import numpy as np

PAD = 0  # pad patch for discritization

# generate score for single traj point

# args:
# traj point
# tree patch (floor(x2) - floor(x1))
# smallest tree rad out of forest

# return:
# integer value for traj point

# steps:
# generate MxM mask of trees where M = dx/(Rmin/2)
# generate some kernel MxM
# dot the mask and kernel
def score(pt,patch,size,rmin):
   ret = 0 # convolution result

   return ret

def get_center_block():
   return

# Divide patch into min tree radius/2 sized
# blocks and bin tree points into a matrix
# MxM.
# ARGS: moth point, tree patch, patch size,
#   min(tree radius)
# RETURNS: matrix MxM, block size, where
#   M = 2*patch/block size (odd)
def discretize(pt,patch,sz,rmin):
  # test with large blocks first
  SZb = rmin/2
  Nb = int(2*sz/SZb)
  # make sure matrix is oddxodd
  Nb += (Nb+1)%2
  mat = np.zeros((Nb,Nb))

  # show moth block bm(0,0)
  mat[Nb/2][Nb/2] = -1

  cnt = 0 #debug
  for tt in patch.values:
     print("tree:"+str(cnt))
     # get deltax, deltay of tree/moth
     tx2px = tt[0] - pt.pos_x
     ty2py = tt[1] - pt.pos_y
     print("dx="+str(ty2py)+", dy="+str(tx2px))
     # get half blocks between mcenter and tcenter
     ihalf = int( 2*tx2px/SZb ) # cols are x
     jhalf = int( 2*ty2py/SZb ) # rows are y
     print("ih="+str(ihalf)+", jh="+str(jhalf))
     bi = ihalf if abs(ihalf) < 2 else int(ihalf/2)
     bj = jhalf if abs(jhalf) < 2 else int(jhalf/2)

     btt = (bi,bj)
     print("bi="+str(bi)+", bj="+str(bj))

     # indicate tree center in matrix index
     Bi = btt[0];
     Bj = btt[1];
     mat[(Nb/2)+Bi][(Nb/2)+Bj] = cnt+1 # show which tree is where
     # mat[(Nb/2)+Bi][(Nb/2)+Bj] = 1

     cnt += 1

  return [mat,SZb]

# sets up tree patch centered on single point
# from moth traj and tree data.
# Also provides visualization of patch by default.
# ARGS: moth_traj, tree_data, bool (opt)
# RETURNS: moth_point, tree_patch, patch_size(L/2)
def setup_test(md,td,display=False):
   # get a single point
   xypoint = md.loc[0] #(int)((len(md)-1)/2)] # midpoint
   xy = xypoint[['pos_x','pos_y']]

   # get patch around single point
   # size is L/2 for patch LxL
   patch_size = (int)(50*max(td.r)/2) + PAD
   l = xy[0]-patch_size < td.x+td.r
   r = td.x-td.r < xy[0]+patch_size
   u = td.y-td.r < xy[1]+patch_size
   d = xy[1]-patch_size < td.y+td.r
   patch = td[l & r & u & d]
   # visualize patch
   if(display):
      plot_frame(xypoint,patch,2*patch_size,td)

   return [xy,patch,patch_size]
