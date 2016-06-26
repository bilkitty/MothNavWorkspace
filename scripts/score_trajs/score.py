#!/usr/bin/python3

from plotStuff import plot_mat
import numpy as np
import scipy.ndimage as ndimage
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

  # Score reflects the average value in product of the mask and kernel.
  # ret = 1 - ret/mask.shape[0]/mask.shape[1]
  score = ret/mask.shape[0]/mask.shape[1]
  return score

oneDGaussian = lambda vbar,v,vsig: np.exp(-1*(vbar-v)**2 / (2*vsig**2))
def gaussian2d(N,meanxy,sigmaxy,amp):
  """
  Computes a single term NxN Gaussian matrix.

  A Gaussian function is computed using tuples `meanxy` and `sigmaxy` which
  specify the center and spread of the Gaussian function, respectively. The
  amplitude is specified by `amp`.

  Parameters
  ----------
  N : int
    Size of Gaussian matrix to return.
  meanxy : tuple
    X and y center. (float)
  sigmaxy : tuple
    X and y standard deviation. (float)
  amp : float
    Amplitude of Gaussian matrix.

  Returns
  -------
  gaussian2d : array_like

  Examples
  --------
  >>> N = 5
  >>> mean = (0,0)
  >>> sigma = (1,1)
  >>> amplitude = 2
  >>> g2 = gaussian2d(N,mean,sigma,amplitude)
  >>> import pylab, numpy, sys
  >>> sys.stdout = pylab.pcolor(numpy.linspace((-N//2),N//2,N)
  ... ,numpy.linspace((-N//2),N//2,N)
  ... ,g2)
  >>> pylab.show()
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
  return amp*np.dot(gaussianx,gaussiany)

def generateKernel(ksize_and_hxhy,means,sigmas,amplitudes,rotate=False):
  """
  Compute an NxN Gaussian kernel with multiple terms.

  If the lengths of Gaussian parameters don't match or the length of
  `ksize_and_hxhy` is not 3, then None is returned. If rotate is true,
  then the kernel is rotated by headingx and headingy contained in
  `ksize_and_hxhy`. Also, kernel size, N, is defined by `ksize_and_hxhy[0]`.

  (!) NOTE: rotation is currently done AFTER the kernel is discretized.

  Parameters
  ----------
  ksize_and_hxhy : array_like
    An array that defines the kernel size, x heading vector, and y
    heading vector, respectively.
  means : array_like
    An array of tuples that specify xmean and ymean respectively. This
    array must be length T where T is the common length between all
    Gaussian parameters (i.e., mean, sigma, amplitude).
  sigmas : array_like
    An array of tuples that specify standard deviation for x and y
    respectively. This array must be length T where T is the common
    length between all Gaussian parameters (i.e., mean, sigma,
    amplitude).
  amplitudes : array_like
    An array of floats that specify amplitude to be used for each
    Gaussian term in the kernel. This array must be length T where T
    is the common length between all Gaussian parameters (i.e., mean,
    sigma, amplitude).
  rotate : bool, optional
    Determines whether the kernel output is rotated. By default, this
    is False.

  Returns
  -------
  kernel : array_like
   An NxN matrix that is a discretization of one or more 2-D Gaussian
   terms in a scoring function.

  Examples
  --------
  >>> sizehxhy = [5,0,0]
  >>> mean = [(0,0)]
  >>> sig = [(10,10)]
  >>> amp = [1]
  >>> generateKernel(sizehxhy,mean,sig,amp)
  array([[ 0.91393119,  0.94530278,  0.95599748,  0.94530278,  0.91393119],
      [ 0.94530278,  0.97775124,  0.98881304,  0.97775124,  0.94530278],
      [ 0.95599748,  0.98881304,  1.      ,  0.98881304,  0.95599748],
      [ 0.94530278,  0.97775124,  0.98881304,  0.97775124,  0.94530278],
      [ 0.91393119,  0.94530278,  0.95599748,  0.94530278,  0.91393119]])
  >>> sizehxhy = [20,0,0]
  >>> mean.append((5,5))
  >>> sig.append((1,1))
  >>> amp.append(2)
  >>> g2d = generateKernel(sizehxhy,mean,sig,amp)

  """
  if (ksize_and_hxhy == None or len(ksize_and_hxhy) != 3):
    print("""(!) score.generateKernel: Invalid ksize_and_hxhy length.
    Needs 3; [N,headingx,headingy].""")
   return None

  M = len(means)
  if (M <= 0):
    print("""(!) score.generateKernel: Invalid length {:d} for Gaussian
    parameters.""".format(M))
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

  # # let's check out what the kernel looks like
  # x = np.linspace(-N//2,(N//2)+1,N)
  # y = np.linspace(-N//2,(N//2)+1,N)
  # pylab.pcolor(x,y,kernel)
  # pylab.show()

  return kernel

def score_trial(trial_data,tcnt,desc,kernel_params,display=False):
  """
  Generate a list of scores, one score value for each frame within a trial.

  Masks contained in `trial_data` are convolved with a kernel matrix to
  yield a score value. The score value is normalized by the dimensions of
  the kernel/mask. The kernel is a 2-D Gaussian defined by `kernel_params`.
  `tcnt` and `desc` provide contextual informaiton about the trial.

  Parameters
  ----------
  trial_data : array_like
    This array should be two nested lists. The outter list should only
    contain a list of mask tuples and a bin size used to generate those
    masks (i.e., [[(masks,data,...,data)],f4].
    See generate_trial_masks.discretize_and_save to see how trials are
    packaged and saved.
  tcnt : int
    Used to identify trial in summary.
  desc : list
    A 4 element list that describes the subject identity and conditions
    used in the trial (i.e., moth_id, flight_speed, fogmin, fogmax)
  kernel_params : array_like
    This is a nested array of that includes the following:
    xymeans - an array of tuples  (i.e., [(m0x,m0y),...,(mTx,mTy)])
    xysigmas - an array of tuples (i.e., [(s0x,s0y),...,(sTx,sTy)])
    amplitudes - an array of int  (i.e., [a0,...,aT])
    These arrays should have the same length, T.
  display : bool, optional
    Plot scores when `display` is true.

  Returns
  -------
  scores : array_like
    A list of score values for each frame in the trial.

  Examples
  -------
  >>> mean = [(0,0)]
  >>> sig = [(10,10)]
  >>> amp = [1]
  >>> description = ["moth1",4,4,8]
  >>> import os
  >>> import pickle
  >>> with open(os.getcwd()+"/test/4_4_8.pickle", 'rb') as handle:
  ...  pdata = pickle.load(handle)

  >>> trial = [k for k in pdata.keys()]
  >>> trial.sort()
  >>> scores = score_trial(pdata[trial[0]]
  ... ,0           # trial number
  ... ,description    # moth and conditions
  ... ,[mean,sig,amp]  # kernel parameters
  ... ,display=False)  #
  -----------------
  Scoring: t0
  Conditions:
    moth_id=moth1
    flight_speed=4.000000
    fogmin=4.000000
    fogmax=8.000000
  Kernel paramters:
    means=[(0, 0)]
    sigmas=[(10, 10)]
    amps=[1]
  ===== SCORE =====
  masks processed: 3454
  cummulative_score: 3741.61132491
  min_score: -1.0
  max_score: 115.365077304
  >>> handle.close()
  """

  print("-----------------")
  print("Scoring: t{:d}".format(tcnt))
  print("Conditions:\n\tmoth_id={:s}\n\tflight_speed={:f}\n\tfogmin={:f}\n\tfogmax={:f}"
    .format(desc[0]
      ,desc[1]
      ,desc[2]
      ,desc[3])
  )
  print("Kernel paramters:\n\tmeans={:s}\n\tsigmas={:s}\n\tamps={:s}"
    .format(str(kernel_params[0])
      ,str(kernel_params[1])
      ,str(kernel_params[2]))
  )

  # extract masks and block size
  data = trial_data[0]
  block_size = trial_data[1]
  trial_masks = data['mat']
  headingxs = data['hx']
  headingys = data['hy']

  # score discretized frames of trajectory
  scores = [0]*len(trial_masks)
  imask = 0 # mask count
  # initialize kernel
  ksize_and_hxhy = [trial_masks[0].shape[0],headingxs[0],headingys[0]]
  kernel = generateKernel(ksize_and_hxhy
    ,kernel_params[0]
    ,kernel_params[1]
    ,kernel_params[2]
    ,rotate=True)

  # score each mask in trial masks
  for sparse_mask in trial_masks:
    mask = sparse_mask.toarray()
    if (kernel_params == 'rotated'):
      # refresh kernel
      ksize_and_hxhy = [trial_masks[imask].shape[0]
        ,headingxs[imask]
        ,headingys[imask]]
      kernel = generateKernel(ksize_and_hxhy
        ,kernel_params[0]
        ,kernel_params[1]
        ,kernel_params[2]
        ,rotate=True)

  # visualize loaded masks
  if (display and imask < 100):
    plot_mat(mask,bsize,"./masks/"+desc[0]
      +'-'+str(int(desc[1]))
      +'-'+str(int(desc[2]))
      +'-'+str(int(desc[3]))
      +'-t'+str(tcnt)
      +'-'+str(imask)+".png")

  # get score
  scores[imask] = score_frame(mask,kernel)
  imask += 1

  print("===== SCORE =====")
  print("masks processed: "+str(imask))
  print("cummulative_score: "+str(sum(scores[0:imask])))
  print("min_score: "+str(min(scores[0:imask])))
  print("max_score: "+str(max(scores[0:imask])))

  return scores[0:imask]

""" DOC TESTS """
if __name__ == "__main__":
  import doctest
  doctest.testmod()
