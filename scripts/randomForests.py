#!/usr/bin/python3

from loadYoyoData import load_data
from plotStuff import plot_scores, plot_mat
import numpy as np
import pandas as pd


SRC = "/home/bilkit/Dropbox/moth_nav_analysis/data/test/csv/forest.csv"
DST = "./"

def createNForests(N,src_filepath=SRC,dst_filepath=DST):
  """
  (int,str,str) -> None

  Given a source file path to the seed forest, create N forests and
  save them as pandas dataframes in a destination path. The destination
  path is the current directory by default and "dest" otherwise.
  """

  # load tree data
  seed_forest = load_data('csv',SRC)
  seed_radii = np.zeros(seed_forest.shape[0],dtype=np.float)

  # measure the mean and stdev of radii
  for i,(x,y) in enumerate(seed_forest[['x','y']].values):
      seed_radii[i] = (x**2 + y**2)**0.5
      if (i % 100) == 0:
        print("{0:d} {1:2f},{2:2f} --> {3:2f}".format(i,x,y,seed_radii[i]))

  # call get stats
  mean_radius, sig_radius = computeNormalStats(seed_radii)
  print("mean = {:2f}\n sig = {:2f}".format(mean_radius,sig_radius))

  # loop over n:
  #   save as csv in dest path
  for iforest in range(N):
    print("processing forest: {0:d}".format(iforest))
    newForest(new_forest,mean_radius,sig_radius)




  return


def newForest(seed,mean,sig):
  """
  (pandas.dataframe, f4, f4) -> (pandas.dataframe)

  Given a pandas data frame of forest data, reproduce a
  new set of forest data sample_size trees.
  >>> newForest(loaded_forest_data,sample_size)
  """
  # once we have mean and stdev, compute N(mean,sigma)
  # and uniform distribution from [0,2pi). Then sample
  # size trees from each dist
  # copy dataframe.values into newForest
  new_forest = seed

  # for all radii (use enumerate to get index to access thetas):
  #   compute (x,y) from theta and radius
  #   overwrite 'x' and 'y' field in newForest at index

  return new_forest

def computeNormalStats(arr):
  """
  (ndarray) -> (tuple(2))
  Given an array (column) of radii, computes and returns the mean
  and standard deviation of the array.
  >>> computeNormalStats(array)
  mean,sigma
  """

  N = arr.shape[0] # expect column
  assert(N != 0), "computeNormalStats: can't calculate mean and sig with array size 0."
  # accumulate values
  mean = arr.sum() / N
  # accumulate squared error
  sig = 0.
  for a in arr:
    sig += (a - mean)**2
  sig = (sig/N)**0.5

  return mean,sig

createNForests(5)



