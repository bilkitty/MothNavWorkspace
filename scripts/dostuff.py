#!/usr/bin/python3

from fileio import load_data
from score import score_trial
from plotStuff import plot_scores, plot_mat
import glob
import pickle
import sys
import os


def main():
  kernel_types = ['uniform','gaussian','rotated']
  pickle_file = "/home/bilkit/Dropbox/moth_nav_analysis/data/masks/original_set/moth1/4_4_8.pickle"
  output_file = "/home/bilkit/Dropbox/moth_nav_analysis/scripts/masks"

  # extract description
  moth_id = pickle_file.split('/')[-2]
  conditions = pickle_file.split('/')[-1]
  conditions = conditions.split('.')[0]
  conditions = conditions.split('_')
  description = [moth_id]
  for c in conditions: description.append(float(c))
  # later, use np array with labels for each index

  # load pickled data
  with open(pickle_file, 'rb') as handle:
    pdata = pickle.load(handle)

  # for each trial in pickle data get discretized frames
  trial = [k for k in pdata.keys()]
  trial.sort() # get trials chronologically for reproducability

  output_file += '/'+moth_id
  scores = []
  tcnt = 1
  # kt = kernel_types[3]
  for kt in kernel_types:

    s = score_trial(pdata[trial[tcnt]],tcnt,description,ktype=kt,display=False)
    scores.append(s)
    # plot_scores(scores,moth_id,tcnt,output_file+"_t"+str(tcnt)+"_"+kt+"_scores.png")

  # # compare different scores
  # import matplotlib.pyplot as plt
  # import numpy as np

  # plt.plot(np.arange(len(scores[0])),scores[0],label="uniform",color='y')
  # plt.plot(np.arange(len(scores[1])),scores[1],label="gaussian",color='r')
  # plt.plot(np.arange(len(scores[2])),scores[2],label="rotated",color='b')
  # plt.title("scores for "+moth_id+" t"+str(tcnt))
  # plt.legend()
  # plt.xlabel("trajectory frame")
  # plt.xlim(-1,len(scores[0])+1)
  # plt.ylabel("score")
  # smin = [min(scores[0]),min(scores[1]),min(scores[2])]
  # smax = [max(scores[0]),max(scores[1]),max(scores[2])]
  # pad = 0.1*(max(smax) - min(smin))
  # plt.ylim(min(smin)-pad,max(smax)+pad+1)
  # plt.show()

  handle.close()

  print("~~Done :)")



  return

main()


