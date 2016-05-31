#!/usr/bin/python3

from loadYoyoData import load_data
from plotStuff import plot_trees
import numpy as np
import math


FOREST_PATH = "/home/bilkit/Dropbox/moth_nav_analysis/data/forests/"

def createNForests(N,src_filepath=FOREST_PATH+"forest.csv",dst_filepath=FOREST_PATH):
  """
  (int,str,str) -> None

  Given a source file path to the seed forest, create N forests and
  save them as pandas dataframes in a destination path. The destination
  path is the current directory by default and "dest" otherwise.
  """

  # load tree data
  seed_forest = load_data('csv',SRC)
  # compute distance between forest center and tree centers
  seed_radii = (seed_forest['x']**2 + seed_forest['y']**2)**0.5

  # compute mean and standard deviation of this distance
  mean_radius, sig_radius = computeNormalStats(seed_radii)
  print("mean = {:2f}\n sig = {:2f}".format(mean_radius,sig_radius))

  # loop over n:
  #   save as csv in dest path
  for iforest in range(N):
    print("processing forest: {0:d}".format(iforest))
    new_forest = seed_forest.copy()
    newForest(new_forest,mean_radius,sig_radius)
    new_radii = (new_forest['x']**2 + new_forest['y']**2)**0.5
    new_mean, new_sig = computeNormalStats(new_radii)
    print("mean = {:2f}\n sig = {:2f}".format(new_mean,new_sig))

    # save tree data as cvs
  return


def newForest(new_forest_template,mean_radius,sigma_radius):
  """
  (pandas.dataframe('x','y','r'), f4, f4) -> None

  Given a pandas data frame of forest data, reproduce a
  new set of forest data sample_size trees. The new distrubution
  >>> newForest(a_forest,mean_radius,sigma_radius)
  """

  # generate new distrubution of trees using normal dist for
  # radii and uniform dist for theta
  sample_size = new_forest_template.shape[0]
  new_radii = np.random.normal(mean_radius,sigma_radius,sample_size)
  new_theta = np.random.uniform(0,2*math.pi,sample_size)

  new_forest_template['x'] = new_radii * np.cos(new_theta)
  new_forest_template['y'] = new_radii * np.sin(new_theta)

  return

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



