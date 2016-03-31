#!/usr/bin/python3

import numpy as np
from loadYoyoData import load_data
import discretize
import pickle
import os

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
   # init filepath for dumping pickle files
   filepath = '../data/trajs/'+dmoth.moth_id[0]
   if not os.path.exists(filepath):
     os.makedirs(filepath)

   # get xy data and conditions description
   traj = dmoth[['pos_x','pos_y']]
   desc = str(int(dmoth.flight_speed[0]))+'_'+\
      str(int(dmoth.fog_min[0]))+'_'+\
      str(int(dmoth.fog_max[0]))

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

   trial_hash['t0'+dmoth.datetime[0]] = trial


   with open(filepath+'/'+desc+'.pickle', 'wb') as handle:
     pickle.dump(trial_hash, handle)

   print("trials: "+str(len(trial_hash)))
   print("trial pts: "+str(len(trial)))
   print("filled: "+str(cnt))

   print("~~Done :)")
   return

main()


