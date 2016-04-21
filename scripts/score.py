#!/usr/bin/python3

from plotStuff import plot_mat
import numpy as np
import scipy.ndimage.interpolation as scipy_interp
import time
import math
import sys
import glob

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
     # ret = 1 - ret/mask.shape[0]/mask.shape[1]
     ret /= mask.shape[0]/mask.shape[1]
   return ret

def split_center(mat,split_size):
   left_edge = (mat.shape[0]/2)*(1-split_size)
   right_edge = (mat.shape[0]/2)*(1+split_size)
   mat[int(left_edge):int(right_edge)+1] = -1
   return

def generateKernel(ktype,mask_data):
   size = mask_data['mat'].shape[0]
   # default: uniform kernel
   ret = np.ones((size,size),dtype=int)
   # opt: center split
   if (ktype == 'center_split'):
      split_center(ret,0.10)
   elif (ktype == 'heading'):
      split_center(ret,0.10)
      theta_rad = math.atan(mask_data['hy']/mask_data['hx'])
      theta_deg = 180*theta_rad/math.pi
      ret = scipy_interp.rotate(ret,theta_deg,mode='nearest',reshape=False)
   elif (ktype == 'gaussian'):
   # generate gaussian distributed kernel
      mean = 0
      stdev = 0.10
   else:
      # do nothing
      return ret


   return ret

# think about keeping data frames as is for simplicity
def score_trial(trial_data,tcnt,desc,ktype='uniform', display=False):
   # measure processing times
   procTime = 0.

   print("Scoring: t"+str(tcnt))
   print("Desc: "+str(desc))
   print("Kernel: "+ktype)

   # extract masks and block size
   trial_masks = trial_data[0]['mat']
   bsize = trial_data[1]

   # score discretized frames of trajectory
   scores = [0]*len(trial_masks)
   mcnt = 0 # mask count
   # initialize kernel
   kernel = generateKernel(ktype,trial_data[0][mcnt])

   for sparse_mask in trial_masks[0:100]:
      mask = sparse_mask.toarray()
      if (ktype == 'heading'):
         # refresh kernel
         kernel = generateKernel(ktype,trial_data[0][mcnt])
      # visualize loaded masks
      if (display and mcnt < 100):
         plot_mat(mask,bsize,"./masks/"+desc[0]
            +'-'+str(int(desc[1]))
            +'-'+str(int(desc[2]))
            +'-'+str(int(desc[3]))
            +'-t'+str(tcnt)
            +'-'+str(mcnt)+".png")

      # get score
      start = time.time()
      scores[mcnt] = score_frame(mask,kernel)
      procTime += time.time() - start

      mcnt += 1

   print("===== SCORE =====")
   print("masks processed: "+str(mcnt))
   print("cummulative_score: "+str(sum(scores[0:mcnt])))
   print("min_score: "+str(min(scores[0:mcnt])))
   print("max_score: "+str(max(scores[0:mcnt])))
   print("==== CPU TIME ====")
   print("avg time (ms) per mask: "+str(round(1000*procTime/mcnt,5)))

   return scores[0:mcnt]