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
  """
  (numpy.ndarray) -> bool

  Returns true if the lengths of each dimension in mat are equal.
  """
  if(mat.shape[0] == 0 or mat.shape[1] == 0):
    print("(!) Mat is flat or empty")
    return False

  return mat.shape[0] == mat.shape[1]

def score_frame(mask,kernel):
  """
  (numpy.ndarray,numpy.ndarray) -> int

  Returns the average value of an element in P, an element-wise product
  of mask and kernel.
  """
  ret = 0 # elem wise mult and sum
  if(is_square_mat(mask) and is_square_mat(kernel)):
    prod = np.multiply(mask,kernel)
    ret = prod.sum()
 # is this meaningful?
 # represent score as percent coverage if kernel is uniform ones
  # ret = 1 - ret/mask.shape[0]/mask.shape[1]
  ret /= mask.shape[0]/mask.shape[1]
  return ret

oneDGaussian = lambda vbar,v,vsig: np.exp(-1*(vbar-v)**2 / (2*vsig**2))
def gaussian2d(N,meanxy,sigmaxy,amp):
  """
  (int,tuple(f4,f4),tuple(f4,f4),f4) -> numpy.ndarray

  Returns an NxN Gaussian matrix with amplitude, mean, and standard dev
  described by meanxy,sigmaxy,amp.
  """

  xbar,ybar = meanxy[0],meanxy[1]
  xsig,ysig = sigmaxy[0],sigmaxy[1]

  # initialize domain
  x = np.linspace(-N//2,(N//2)+1,N)
  y = np.linspace(-N//2,(N//2)+1,N)
  # reshape numpy array to column vector Nx1
  gaussianx = oneDGaussian(xbar,x,xsig).reshape(N,1)
  # reshape numpy array to row vector 1xN
  gaussiany = oneDGaussian(ybar,y,ysig).reshape(1,N)
  # compute dot product of x and y
  gaussian2d = amp*np.dot(gaussianx,gaussiany)
  # let's check out what the kernel looks like
  pylab.pcolor(x,y,gaussian2d)
  pylab.show()

  return gaussian2d

# instead of ktype, pass kernel function (e.g., 2d gaussian function)
def generateKernel(ksize_and_hxhy,means,sigmas,amplitudes,rotate=False):
  """
  ([int,f4,f4]
    ,numpy.ndarray(tuple(f4,f4))
    ,numpy.ndarray(tuple(f4,f4))
    ,numpy.ndarray(f4)
    ,bool)
  -> ndarray(ndarray)

  Given [N,headingx,headingy] and M sets of gaussian parameters (mean,
  stdev,amplitude), compute an NxN Gaussian kernel. If the lengths of gaussian
  parameters don't match or the lenght of ksize_and_hxhy is not 3, then None is
  returned. Otherwise, return an unrotated kernel by default and a rotate kernel
  if rotate is True.

  Examples:
  >>> sizehxhy = [5,0,0]
  >>> mean = [(0,0)]
  >>> sig = [(10,10)]
  >>> amp = [1]
  >>> g2d = generateKernel(sizehxhy,mean,sig,amp)
  array([[ 0.91393119,  0.94530278,  0.95599748,  0.94530278,  0.91393119],
         [ 0.94530278,  0.97775124,  0.98881304,  0.97775124,  0.94530278],
         [ 0.95599748,  0.98881304,  1.        ,  0.98881304,  0.95599748],
         [ 0.94530278,  0.97775124,  0.98881304,  0.97775124,  0.94530278],
         [ 0.91393119,  0.94530278,  0.95599748,  0.94530278,  0.91393119]])
  """
  if (ksize_and_hxhy == None or len(ksize_and_hxhy) != 3):
    print("""(!) score.generateKernel: Invalid ksize_and_hxhy length.
      Needs 3; [N,headingx,headingy].""")
    return None

  M = len(means)
  if (len(sigmas) != M or len(amplitudes) != M):
    print("""(!) score.generateKernel: Lengths of Gaussian parameter arrays
      don't match; len of means,sigs,amps = {:d},{:d},{:d}""".format(len(means)
        ,len(sigmas)
        ,len(amplitudes)))
    return None

  N = ksize_and_hxhy[0]
  kernel = np.zeros((N,N),dtype=float)

  # Normalize the kernel by M... not sure if this is what should be done
  for term in range(M):
    kernel += (1./M)*gaussian2d(N,means[term],sigmas[term],amplitudes[term])

  if (rotate):
    theta_rad = math.atan(ksize_and_hxhy[2]/ksize_and_hxhy[1])
    theta_deg = 180*theta_rad/math.pi
    kernel = ndimage.interpolation.rotate(kernel,theta_deg
      ,mode='nearest',reshape=False)

  return kernel

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