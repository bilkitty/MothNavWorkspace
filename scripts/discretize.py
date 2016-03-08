#!/usr/bin/python3

import numpy as np
import pandas as pd
import sys

# computes matrix indices as ith-block and
# jth-block between tcenter and origin.
def map_to_mat_idx(tcenter,orig,bsize):
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
def discretize(pt,patch,sz,rmin):
  xerror = 0
  yerror = 0
  # use np arrays
  if(isinstance(pt,pd.Series)):
    pt = pt.values
  if(isinstance(patch,pd.DataFrame)
    or isinstance(patch,pd.Series)):
    patch = patch.values

  if(rmin < 0):
    print("(!) Negative rmin")
    return None
  # get block size
  SZb = rmin/2

  # initialize matrix
  Nb = int(2*sz/SZb)
  # make sure matrix is oddxodd and not ridiculously large
  Nb += (Nb+1)%2
  if(sys.maxsize < Nb):
    print("(!) outrageous mat size, block size is too small")
    return None

  # init matrix that hold binary values
  mat = np.zeros((Nb,Nb),dtype=int)
  min_idx = 0
  max_idx = mat.shape[0]-1

  # show moth block bm(0,0)
  mat[int(Nb/2)][int(Nb/2)] = -1

  cnt = 1 #debug
  for tt in patch:
     # get tree center
     itt = map_to_mat_idx(tt,pt,SZb)
     Mi = int(Nb/2)+itt[0];
     Mj = int(Nb/2)+itt[1];

     # convert tree radius to nblocks
     # rr =  tt[2]*(2**.5) # length from center to CORNER of sq = tradius
     # rr /= 2
     rr = tt[2] # length from center to SIDE of sq = tradius
     rb = map_to_mat_idx((tt[0]+rr,tt[1]),tt,SZb)

     # set indices of mat[ti,tj] using mask
     # handle trees partially cuttoff
     xmin = keep_in_bounds(Mi - rb[0], min_idx, max_idx)
     xmax = keep_in_bounds(Mi + rb[0], min_idx, max_idx)
     ymin = keep_in_bounds(Mj - rb[0], min_idx, max_idx)
     ymax = keep_in_bounds(Mj + rb[0], min_idx, max_idx)

     # create mask of ones over center+root(2)/2
     xsize = xmax - xmin
     ysize = ymax - ymin
     mask = cnt*np.ones((xsize+1,ysize+1),dtype=int)
     mask = mask.T

     # apply mask over tree center (within boundaries of mat)
     mat[xmin:xmax+1].T[ymin:ymax+1] = np.bitwise_or(mat[xmin:xmax+1].T[ymin:ymax+1],mask)

     # mark tree center (help see center of partically cuttoff tree)
     if(Mi < 0 or Mj < 0 or Nb <= Mi or Nb <= Mj):
       print("  tree:"+str(cnt))
       print("    Center out of bounds: (Mi,Mj)=("+str(Mi)+","+str(Mj)+")")
       print("    xmin,xmax:"+str(xmin)+","+str(xmax)+" ymin,ymax:"+str(ymin)+","+str(ymax))
       print("    radius: "+str(rb[0]))
     else:
       mat[Mi][Mj] = -1*cnt

     # view error in reconstructing xy distance b/w tree and moth center
     xerr = abs(tt[0]-itt[0]*SZb-pt[0])
     xerror += xerr
     yerr = abs(tt[1]-itt[1]*SZb-pt[1])
     yerror += yerr

     cnt += 1

  print("  avg xerror = avg(tx - ii*bsz-px) = "+str(round(xerror/cnt,5)))
  print("  avg yerror = avg(ty - jj*bsz-py) = "+str(round(yerror/cnt,5)))
  return [mat,SZb]
