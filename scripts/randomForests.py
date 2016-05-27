#!/usr/bin/python3

from loadYoyoData import load_data
from plotStuff import plot_scores, plot_mat
import numpy as np

def createNewForest():
  """
  (pandas.dataframe) -> (ndarray)

  Given a pandas data frame of forest data, reproduce a
  new set of forest data sample_size trees.
  >>> createNewForest(loaded_forest_data,sample_size)
  new_forest
  """
  # copy dataframe.values into newForest
  # radii

  # compute the mean of radii
  # for all (x,y) pairs:
  #   convert to radius

  # call get stats

  # once we have mean and stdev, compute N(mean,sigma)
  # and uniform distribution from [0,2pi). Then sample
  # size trees from each dist

  # for all radii (use enumerate to get index to access thetas):
  #   compute (x,y) from theta and radius
  #   overwrite 'x' and 'y' field in newForest at index

  return

def computeNormalStats():
  """
  (ndarray) -> (tuple(2))
  Given an array of radii, computes and returns the mean
  and standard deviation of the array.
  >>> computeNormalStats(array)
  mean,sigma
  """

  # take the sum of radii and div by size

  # compute stdv of radii
  # for all radii:
  #   compute difference between radius and mean
  #   acummulate square of difference

  return





