#!/usr/bin/python3

import numpy as np
import pandas as pd
import sys
import math
from scipy.sparse import bsr_matrix

PAD = 1  # patches are padded with PAD*max(tree radius)

# inserts mat and point data to numpy array
# so that it can be processed independently from
# raw trajectory data.
# if requested index is out of bounds, then the
# boundary indices are overwritten.
def pack(mat,data,ii,l):
  if (ii < 0 or len(l) <= ii):
    print("pack: warn: overwritting list data")
  bounded_index = min(max(ii,0),len(l))
  sparse_mat = bsr_matrix(mat).tobsr()
  l[bounded_index] = (sparse_mat,data[0],data[1],data[2],data[3])
  return

# generates data frame slice of env objects
# contained within a square around origin.
# ARGS: origin (to center patch on), forest
# RETURNS: tree patch, patch size (L/2 of
# patch, not number of trees)
def get_patch(orig,env):
   patch_size = (int)(max(env.r)*(10 + PAD)) # floored
   # includes trees whose radius is entirely contianed
   # in the frame boundary
   l = orig[0]-patch_size < env.x-env.r
   r = env.x+env.r < orig[0]+patch_size
   u = env.y+env.r < orig[1]+patch_size
   d = orig[1]-patch_size < env.y-env.r
   patch = env[l & r & u & d]
   return [patch, patch_size]

# computes matrix indices as ith-block and
# jth-block between tcenter and origin.
def map_to_mat_idx(tcenter,orig,bsize):
  # avoid divide by zero or neg
  if (bsize <= 0):
    print("(!) map_to_mat_idx: invalid bsize "+str(bsize))
    return (float('NaN'),float('NaN'))

  # use np arrays
  if(isinstance(orig,pd.Series)):
    orig = orig.values

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

def keep_in_bounds(val,vmin,vmax):
  if(val < vmin):
    return vmin
  if(vmax < val):
    return vmax
  return val

def is_edge_idx(idx,msize):
  return (idx == 0) or (idx == msize - 1)

# divide patch into min tree radius/2 sized
# blocks and bin tree points into a matrix
# MxM.
# ARGS: moth point, tree patch, patch size,
#   min(tree radius)
# RETURNS: matrix MxM, block size, where
#   M = 2*patch/block size (odd)
#   returns block size = -1 if error
def discretize(pt,patch,sz,rmin):
  # use np arrays
  if(isinstance(pt,pd.Series)):
    pt = pt.values
  if(isinstance(patch,pd.DataFrame)
    or isinstance(patch,pd.Series)):
    patch = patch.values

  if(rmin < 0):
    print("(!) Negative rmin")
    return [None,-1]
  # get block size
  SZb = rmin/2

  # initialize matrix
  Nb = int(2*sz/SZb)
  # make sure matrix is oddxodd and not ridiculously large
  Nb += (Nb+1)%2
  if(sys.maxsize < Nb):
    print("(!) outrageous mat size, block size is too small")
    return [None,-1]

  # init matrix that hold binary values
  mat = np.zeros((Nb,Nb),dtype=int)

  # mark moth block bm(0,0)
  mat[int(Nb/2)][int(Nb/2)] = -1

  for tt in patch:
    # get tree center (block size should be non-zero)
    itt = map_to_mat_idx(tt,pt,SZb)

    # convert tree radius to nblocks
    rr = tt[2] # length from center to EDGE of sq = tradius
    rr2 = rr**2
    rr_root2_by2 = (2**0.5)*rr / 2 # length from center to CORNER of sq = tradius
    [rb,tmp] = map_to_mat_idx((tt[0]+rr,tt[1]),tt,SZb)
    [rb_root2_by2,tmp] = map_to_mat_idx((tt[0]+rr_root2_by2,tt[1]),tt,SZb)

    # create a mask of 1's centered on tree
    tsize = 2*rb + 1
    mask = np.ones((tsize,tsize),dtype=int)
    # trim mask
    for i in range(0,tsize):
      # offset defines the beginning of the range of columns to analyse
      offset = 2*rb_root2_by2
      if (i <= rb - rb_root2_by2 or rb + rb_root2_by2 <= i):
        offset = 0
      # check that distance from center to block is < tree radius
      for j in range(0, rb - rb_root2_by2):
        if (rr2 < ((i-rb)*SZb)**2 + ((j-rb)*SZb)**2):
          print(str(((i-rb)*SZb)**2 + ((j-rb)*SZb)**2)+'>'+str(rr2))
          mask[i][j] = 0

      for j in range(rb - rb_root2_by2 + offset,tsize):
        if (rr2 < ((i-rb)*SZb)**2 + ((j-rb)*SZb)**2):
          print(str(((i-rb)*SZb)**2 + ((j-rb)*SZb)**2)+'>'+str(rr2))
          mask[i][j] = 0

    # apply mask over tree center (within boundaries of mat)
    xmin,xmax = itt[0] - rb + int(Nb/2), itt[0] + rb + int(Nb/2)
    ymin,ymax = itt[1] - rb + int(Nb/2), itt[1] + rb + int(Nb/2)
    mat[xmin:xmax+1].T[ymin:ymax+1] = np.bitwise_or(mat[xmin:xmax+1].T[ymin:ymax+1],mask)
    # mark tree center
    icenter = int(Nb/2)+itt[0];
    jcenter = int(Nb/2)+itt[1];
    mat[icenter][jcenter] = -1

  from plotStuff import plot_mat
  plot_mat(mat,SZb)

  return [mat,SZb]
