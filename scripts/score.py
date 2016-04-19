#!/usr/bin/python3

from plotStuff import plot_mat
import numpy as np
import time
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

def generateKernel(ktype,size):
   # default: uniform kernel
   ret = np.ones((size,size),dtype=int)
   # opt: vertical split
   if(ktype == 'vertical_split'):
      split_size = int(ret.shape[0] / 10)
      ret[(ret.shape[0]/2)-split_size:(ret.shape[0]/2)+split_size+1] = -1

   return ret

# think about keeping data frames as is for simplicity
def score_trial(trial_data,tcnt,desc,ktype='uniform', display=False):
   # measure processing times
   procTime = 0.

   print("Scoring: t"+str(tcnt))
   print("Desc: "+str(desc))
   print("Kernel: "+ktype)

   # extract masks and block size
   trial_masks = trial_data[0]
   bsize = trial_data[1]

   # score discretized frames of trajectory
   scores = [0]*len(trial_masks)
   mcnt = 0 # mask count
   for sparse_mask in trial_masks[0:100]:
      mask = sparse_mask.toarray()
      # initialize kernel
      kernel = generateKernel(ktype,mask.shape[0])
      # visualize loaded masks
      if (display and mcnt < 100):
         plot_mat(mask,bsize,"./masks/"+desc[0]
            +'-'+str(int(desc[1]))
            +'-'+str(int(desc[2]))
            +'-'+str(int(desc[3]))
            +'-t'+str(tcnt)
            +'-'+str(mcnt)+".png")

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