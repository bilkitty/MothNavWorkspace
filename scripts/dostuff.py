#!/usr/bin/python3

from loadYoyoData import load_data
from score import score_trial
from plotStuff import plot_scores, plot_mat
import glob
import pickle
import sys
import os


def main():
   kernel_types = ['uniform','vertical_split','gaussian','heading']
   pickle_file = "/home/bilkit/Dropbox/moth_nav_analysis/data/masks/moth1/4_4_8.pickle"
   output_file = "/home/bilkit/Dropbox/moth_nav_analysis/scripts/masks"

   # extract desctiption
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
   kt = kernel_types[1]
   for tcnt in range(0,len(trial)):
      scores = score_trial(pdata[trial[tcnt]],tcnt,description,ktype=kt)
      plot_scores(scores,moth_id,tcnt,output_file+"_t"+str(tcnt)+"_"+kt+"_scores.png")

   handle.close()

   print("~~Done :)")



   return

main()


