#!/usr/bin/python3

from plotStuff import plot_mat
import numpy as np
import scipy.ndimage as ndimage
import time
import math
import pylab
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

# instead of ktype, pass kernel function (e.g., 2d gaussian function)
def generateKernel(ktype,mask_data):
  N = mask_data['mat'].shape[0]
  amplitude = 1
  # gaussian function (pass this as arg)
  oneDGaussian = lambda vbar,v,vsig: math.exp(-1*(vbar-v)**2 / (2*vsig**2))
  # oneDGaussian = lambda vbar,v,vsig: numpy.exp(-1*(vbar-v)**2 / (2*vsig**2))
  # g2d = lambda x,y,A,Rmean,Rstdev: A*math.exp((-1/(2*Rstdev**2))+
  #   A*math.exp((-1/(2*Rstdev**2))*((-1*Rmean-y)**2+(-1*Rmean-x)**2)))
  # initialize domain
  x = np.linspace(-N//2,(N//2)+1,N)
  y = np.linspace(-N//2,(N//2)+1,N)
  # fill in the kernel using desired function
  xbar,ybar = 0,0
  xsig,ysig = 10,10
  gaussian2d = np.zeros((N,N))
  for i in range(0,N):
    for j in range(0,N):
      gaussian2d[i,j] = amplitude*oneDGaussian(xbar,x[i],xsig)*oneDGaussian(ybar,y[j],ysig)
      # gaussian2d[i,j] = g2d(x[i],y[j],.5,0,10)

  # let's check out what the kernel looks like
  pylab.pcolor(x,y,gaussian2d)
  pylab.show()

  if (ktype == 'rotated'):
    theta_rad = math.atan(mask_data['hy']/mask_data['hx'])
    theta_deg = 180*theta_rad/math.pi
    gaussian2d = ndimage.interpolation.rotate(gaussian2d,theta_deg,mode='nearest',reshape=False)

  return gaussian2d

# think about keeping data frames as is for simplicity
def score_trial(trial_data,tcnt,desc,ktype='uniform', display=False):
  # measure processing times [score,genkernel]
  procTime = [0.]*2

  print("-----------------")
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
  start = time.time()
  kernel = generateKernel(ktype,trial_data[0][mcnt])
  procTime[1] += time.time() - start

  # for sparse_mask in trial_masks[0:100]:
  for sparse_mask in trial_masks:
    mask = sparse_mask.toarray()
    if (ktype == 'rotated'):
      # refresh kernel
      start = time.time()
      kernel = generateKernel(ktype,trial_data[0][mcnt])
      procTime[1] += time.time() - start

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
    procTime[0] += time.time() - start

    mcnt += 1

    print("===== SCORE =====")
    print("masks processed: "+str(mcnt))
    print("cummulative_score: "+str(sum(scores[0:mcnt])))
    print("min_score: "+str(min(scores[0:mcnt])))
    print("max_score: "+str(max(scores[0:mcnt])))
    print("==== CPU TIME (ms) ====")
    print("generating kernel: "+str(round(1000*procTime[1],5)))
    print("processing masks: "+str(round(1000*procTime[0],5)))
    print("avg per mask: "+str(round(1000*procTime[0]/mcnt,5)))
    print("cummulative kernel and mask: "+str(round(1000*sum(procTime),5)))

  return scores[0:mcnt]