#!/usr/bin/python3

import numpy as np
from loadYoyoData import load_data
import discretize

def main():
   # read tree data
   dtree = load_data("csv","../data/test/csv/forest.csv")

   # load trajectories
   dmoth = load_data("csv","../data/test/csv/moth6_single.csv")    # check for loaded files
   print( "Processing points: "+str(len(dmoth.values)) )
   print( "Forest size: "+str(len(dtree.values)) )

   # initialize dictionary
   trial_hash = {}

   # check that moth and tree data are not empty
   if(len(dtree)+len(dmoth) == 0):
      printf("(!) ERROR: No data loaded.")
      return

   # for each trajectory:
   # init np that can contain mats (i.e., dtype = object)
   trial = np.zeros(len(dmoth.values),dtype=object)

   # get xy data
   traj = dmoth[['pos_x','pos_y']]

   cnt = 0
   # process other points
   for point in traj.values[:10]:
      print("pt "+str(cnt)+" ("+str(round(point[0],3))+","+str(round(point[1],3))+"):",end='')
      # get scoring region, may contain trees
      [patch,sz] = discretize.get_patch(point,dtree)
      print("\t"+str(len(patch.values))+" ts")
      # discretize that shit
      [mask, bsize] = discretize.discretize(point,patch,sz,min(dtree.r))
      # save mask
      discretize.pack(mask,cnt,trial)

      cnt += 1

   trial_hash['t0'] = trial

   print("trials: "+str(len(trial_hash)))
   print("trial pts: "+str(len(trial)))
   print("filled: "+str(cnt))

   print("~~Done :)")
   return

main()

# import pickle

# a = {'hello': 'world'}

# with open('filename.pickle', 'wb') as handle:
#   pickle.dump(a, handle)

# with open('filename.pickle', 'rb') as handle:
#   b = pickle.load(handle)

# print a == b