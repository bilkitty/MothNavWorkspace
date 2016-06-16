#!/usr/bin/python3

import numpy as np
import pandas as pd
import sys
from scipy.sparse import bsr_matrix

PAD = 1  # patches are padded with PAD*max(tree radius)

def pack(mat,data,ii,arr):
  """
  (ndarray,[double*(4)],int,ndarray)-> None
  Converts a matrix to a sparse mat then creates a tuple containing
  this sparse matrix and the elements from data list. This tuple is
  inserted to the array at ii. We check that ii is within the bounds
  of the array. If ii exceeds the boundaries of the array, then the
  edges (i.e., 0 and len(array)-1) are overwritten; and a warning is
  uttered.
  """
  if (ii < 0 or len(arr) <= ii):
    print("pack: warn: overwritting list data")
  bounded_index = min(max(ii,0),len(arr))
  sparse_mat = bsr_matrix(mat).tobsr()
  arr[bounded_index] = (sparse_mat,data[0],data[1],data[2],data[3])
  return

def get_patch(origin,env):
  """
  ([double*(2)],pandas.dataframe) -> [pandas.dataframe,int]
  Returns a slice of the forest that is within a square
  neighborhood, described as patch_size, about the origin.
  The trees are included in the neighborhood if they entirely
  fall in the boundary of the neighborhood. In other words,
  all the tree's surface is within the square boundary.
  """
  patch_size = (int)(max(env.r)*(10 + PAD))
  l = origin[0]-patch_size < env.x-env.r
  r = env.x+env.r < origin[0]+patch_size
  u = env.y+env.r < origin[1]+patch_size
  d = origin[1]-patch_size < env.y-env.r
  patch = env[l & r & u & d]
  return [patch, patch_size]

# computes matrix indices as ith-block and
# jth-block between tcenter and origin.
def map_to_mat_idx(tcenter,origin,bsize):
  """
  (ndarray,ndarray,int) -> (int,int)
  Computes the distance between tree center and
  origin in units of block size. Since the origin
  is meant to be at the center of an odd grid,
  the distance is computed as a count of half
  blocks. Then this count is converted to whole
  blocks in the x and y direction and returned
  as a tuple.
  """
  # avoid divide by zero or neg
  if (bsize <= 0):
    print("(!) map_to_mat_idx: invalid bsize "+str(bsize))
    return (float('NaN'),float('NaN'))

  # get deltax, deltay
  tx2px = tcenter[0] - origin[0]
  ty2py = tcenter[1] - origin[1]
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
#   returns block size = -1 if error
def discretize(pt,patch,sz,rmin):
  # convert dataframes to numpy arrays
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
          mask[i][j] = 0

      for j in range(rb - rb_root2_by2 + offset,tsize):
        if (rr2 < ((i-rb)*SZb)**2 + ((j-rb)*SZb)**2):
          mask[i][j] = 0

    # apply mask over tree center (within boundaries of mat)
    xmin,xmax = itt[0] - rb + int(Nb/2), itt[0] + rb + int(Nb/2)
    ymin,ymax = itt[1] - rb + int(Nb/2), itt[1] + rb + int(Nb/2)
    mat[xmin:xmax+1].T[ymin:ymax+1] = np.bitwise_or(mat[xmin:xmax+1].T[ymin:ymax+1],mask)
    # mark tree center
    icenter = int(Nb/2)+itt[0];
    jcenter = int(Nb/2)+itt[1];
    mat[icenter][jcenter] = -1

  return [mat,SZb]
