#!/usr/bin/python3

import numpy as np
import pandas as pd
import sys
from scipy.sparse import bsr_matrix

PAD = 1  # patches are padded with PAD*max(tree radius)

def pack(mat,data,ii,arr):
  """
  (numpy.ndarray,[double*(4)],int,numpy.ndarray)-> None

  Converts a matrix to a sparse mat then creates a tuple containing
  this sparse matrix and the elements from data list. This tuple is
  inserted to the array at ii. We check that ii is within the bounds
  of the array. If ii exceeds the boundaries of the array, then the
  edges (i.e., 0 and len(array)-1) are overwritten; and a warning is
  uttered. If data is not length 4, then a warning message is given
  and NaN values are packed into the array.
  """
  if (data == None or len(data) != 4):
    print("discretize.pack: WARN: Data is invalid length.")
    data=[float('NaN')]*4
  if (ii < 0 or len(arr) <= ii):
    print("discretize.pack: WARN: Overwritting list data")
  bounded_index = min(max(ii,0),len(arr))
  sparse_mat = bsr_matrix(mat).tobsr()
  arr[bounded_index] = (sparse_mat,data[0],data[1],data[2],data[3])
  return

def get_patch(origin,forest):
  """
  ([double*(2)],pandas.dataframe) -> [pandas.dataframe,int]

  Returns a slice of the forest that is within a square
  neighborhood, described by patch_size*2, about the origin.
  The trees are included in the neighborhood if they entirely
  fall in the boundary of the neighborhood. In other words,
  all the tree's surface is within the square boundary.

  Example:
  (see discretize)
  """
  patch_size = (int)(max(forest.r)*(10 + PAD))
  l = origin[0]-patch_size < forest.x-forest.r
  r = forest.x+forest.r < origin[0]+patch_size
  u = forest.y+forest.r < origin[1]+patch_size
  d = origin[1]-patch_size < forest.y-forest.r
  patch = forest[l & r & u & d]
  return [patch, patch_size]

def map_to_mat_idx(tcenter,origin,bsize):
  """
  (numpy.ndarray,numpy.ndarray,int) -> (int,int)

  Computes the distance between tree center and origin in units of
  block size. Since the origin is meant to be at the center of an
  odd grid, the distance is computed as a count of half blocks.
  Then this count is converted to whole blocks in the x and y
  direction and returned as a tuple. If block size is not valid,
  i.e., negative or zero, then (NaN,NaN) is returned.

  Example:
  >>> from fileio import load_dataframe
  >>> trees = load_dataframe("csv",dump+"/trees.csv")
   loading: /home/bilkit/Dropbox/moth_nav_analysis/scripts/test/trees.csv
  >>> tree = trees.values[0]
  >>> bin_size = min(trees.r)/2
  >>> [binned_radius,tmp] = map_to_mat_idx((tree[0]+tree[2],tree[1])
    ,tree
    ,bin_size)
  >>> binned_radius,tmp
  (2, 0)
  """
  # avoid divide by zero or neg
  if (bsize <= 0):
    print("(!) discretize.map_to_mat_idx: Invalid bsize "+str(bsize))
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

def discretize(point,patch,patch_size,minimum_radius):
  """
  (numpy.ndarray,pandas.dataframe or Series,int,int) -> [numpy.ndarray,int]

  Given a dataframe of trees, quantize the (x,y,r) of the trees and create a
  binary mask that represents trees with ones. The point (x,y) defines the
  center of the mask, which is always odd. The mask and the bin size are
  returned. If the minimum radius is negative or the bin size is too small,
  then [None,-1] is returned.

   Examples:
   >>> from fileio import load_dataframe
   >>> from plotStuff import plot_mat
   >>> import os
   >>> dump = os.getcwd()+"/test"
   >>> traj = load_dataframe("h5",dump+"/moth1_448f0.h5")
   loading: /home/bilkit/Dropbox/moth_nav_analysis/scripts/test/moth1_448f0.h5
   >>> point = traj[["pos_x","pos_y"]].iloc[400]
   >>> trees = load_dataframe("csv",dump+"/trees.csv")
   loading: /home/bilkit/Dropbox/moth_nav_analysis/scripts/test/trees.csv
   >>> patch,size = get_patch(point,trees)
   >>> [mask, bsize] = discretize(point,patch,size,min(trees.r))
   >>> plot_mat(mask,bsize,targ_file=dump+"/discretize.png")
   plotting mat(111x111)
  """
  # convert dataframes to numpy arrays
  if(isinstance(point,pd.Series)):
    point = point.values
  if(isinstance(patch,pd.DataFrame)
    or isinstance(patch,pd.Series)):
    patch = patch.values

  if(minimum_radius < 0):
    print("(!) discretize.discretize: Negative minimum_radius")
    return [None,-1]
  # get block size
  bin_size = minimum_radius/2

  # initialize matrix
  n_bins = int(2*patch_size/bin_size)
  # make sure matrix is oddxodd and not ridiculously large
  n_bins += (n_bins+1)%2
  if(sys.maxsize < n_bins):
    print("(!) discretize.discretize: Outrageous mat size, block size is too small")
    return [None,-1]

  # init matrix that hold binary values
  mat = np.zeros((n_bins,n_bins),dtype=int)

  # mark moth block bm(0,0)
  mat[int(n_bins/2)][int(n_bins/2)] = -1

  for tree in patch:
    # get tree center (block size should be non-zero)
    binned_tree_loc = map_to_mat_idx(tree,point,bin_size)

    # convert tree radius to nblocks
    radius = tree[2] # length from center to EDGE of sq = tradius
    radius_squared = radius**2
    radius_root2_by2 = (2**0.5)*radius / 2 # length from center to CORNER of sq = tradius
    [binned_radius,tmp] = map_to_mat_idx((tree[0]+radius,tree[1])
      ,tree
      ,bin_size)
    [binned_radius_root2_by2,tmp] = map_to_mat_idx((tree[0]+radius_root2_by2,tree[1])
      ,tree
      ,bin_size)

    # create a sub-mask of 1's centered on tree (+1 accounts for tree center)
    l_outter_square = 2*binned_radius + 1
    l_inner_square = 2*binned_radius_root2_by2 + 1
    mask = np.ones((l_outter_square,l_outter_square),dtype=int)
    # trim sub-mask to approximate a circular tree
    for row in range(0,l_outter_square):
      offset = l_inner_square - 1
      inner_left_edge = binned_radius - binned_radius_root2_by2
      inner_right_edge = binned_radius + binned_radius_root2_by2
      # inspect all columns if row is not in the inner square, otherwise only
      # inspect the columns that are in the outter square.
      if (row <= inner_left_edge or inner_right_edge <= row):
        offset = 0
      # inspection: check that distance from center to block is < tree radius
      for col in range(0, inner_left_edge):
        if (radius_squared < ((row-binned_radius)*bin_size)**2 + ((col-binned_radius)*bin_size)**2):
          mask[row][col] = 0
      for col in range(inner_left_edge + offset,l_outter_square):
        if (radius_squared < ((row-binned_radius)*bin_size)**2 + ((col-binned_radius)*bin_size)**2):
          mask[row][col] = 0

    # apply mask over tree center (within boundaries of mat)
    xmin,xmax = binned_tree_loc[0] - binned_radius + int(n_bins/2), binned_tree_loc[0] + binned_radius + int(n_bins/2)
    ymin,ymax = binned_tree_loc[1] - binned_radius + int(n_bins/2), binned_tree_loc[1] + binned_radius + int(n_bins/2)
    mat[xmin:xmax+1].T[ymin:ymax+1] = np.bitwise_or(mat[xmin:xmax+1].T[ymin:ymax+1],mask)
    # mark tree center
    icenter = int(n_bins/2)+binned_tree_loc[0];
    jcenter = int(n_bins/2)+binned_tree_loc[1];
    mat[icenter][jcenter] = -1

  return [mat,bin_size]
