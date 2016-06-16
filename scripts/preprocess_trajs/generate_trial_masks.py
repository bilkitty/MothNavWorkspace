#!/usr/bin/python3

import numpy as np
from loadYoyoData import load_dataframe
import discretize
import pickle
import glob
import os

def discretize_and_save(trial_hash,forest,traj,trial_id,trial_datetime):
   """
   (dict,pandas.dataframe,pandas.dataframe,str,trial_datetime) -> None

   Generates a set of discretized frames for a given trajectory and forest.
   It is expected that traj is a dataframe of x,y,headingx,headingy data.
   For each point, a sparse matrix is computed that describes the forest
   environment near it. This point is packed, with its corresponding frame,
   into an array. This array is stored in the dictionary, trial_hash, using
   the key trial_id/datetime.
   """
   pt_cnt = 0
   bsize = 0
   # array of mat,data pairs
   trial = np.zeros(len(traj),dtype=[('mat','O')
      ,('x', '<f4'), ('y', '<f4')
      ,('hx', '<f4'), ('hy', '<f4')])
   # process other points from
   for point in traj.values:
      xy = point[0:2] #
      # get scoring region, may contain trees
      [patch,sz] = discretize.get_patch(xy,forest)
      # discretize that shit
      [mask, bsize_temp] = discretize.discretize(xy,patch,sz,min(forest.r))
      bsize = max(bsize_temp,bsize)
      # save mask, trial count, and block size
      if (0 < bsize_temp):
         discretize.pack(mask,point,pt_cnt,trial)
      else:
         print("(!) processTrial: failed to compute mask for "+trial_id+"["+str(pt_cnt)+"]")

      pt_cnt += 1

   trial_hash[trial_id+'_'+str(trial_datetime)] = [trial,bsize]

   print(trial_id)
   print("len: "+str(len(trial)))

   return

def writeToFile(file_name,txt):
   """
   (str,str) -> None

   Write text to an opened file. The text is converted to
   eight byte unicode before it is written to file.
   """
   file_name.write(bytes(txt+'\n','UTF-8'))
   return

def processTrials(batch_o_trials,forest,filepath_prefix,logfile):
   """
   (array of str,pandas.dataframe,str,str) -> None
   Loads a data frame from each file path in the list and transforms it
   into an array of discretized frames. These frames are saved into a
   dictionary of the corresponding mothid. The dictionary of trials is
   saved into a pickle labeled with the trial conditions.
   """
   # trial and current mothid
   trial_cnt = 0
   mothname = ""
   # conditions of the experiment are embedded in the pickle file name
   # i.e., desc = 'flightspeed_fogmin_fogmax'
   filepath,desc = "",""
   # initialize trial dictionary
   # key = trialid_datetime, val = [trial,block_size]
   trial_hash = {}

   """ PROCESS EACH TRIAL INTO STACK OF MASKS """
   for st in batch_o_trials:
      raw_data = load_dataframe("h5",st)
      print( "Processing points: "+str(len(raw_data.values)) )
      # skip processing if dataframe is empty
      if(len(raw_data) == 0):
         print("(!) ERROR: No moth data loaded for "+st)
         continue

      new_moth = raw_data.moth_id.iloc[0]
      # get a description of conditions
      desc = str(int(raw_data.flight_speed.iloc[0]))+'_'+\
         str(int(raw_data.fog_min.iloc[0]))+'_'+\
         str(int(raw_data.fog_max.iloc[0]))

      # setup a directory (named after mothid) to store pickle files
      filepath = filepath_prefix+'/'+new_moth
      if not os.path.exists(filepath):
        os.makedirs(filepath)

      # We save a group of trials into a pickle file for each mothid
      # This condition only occurs when the mothid changes (i.e., the
      # previous set of trials is saved).
      if (mothname != "" and mothname != new_moth):
         print(mothname+": saving "+str(trial_cnt)+" trajs in "+filepath+'/'+desc+".pickle")
         with open(filepath+'/'+desc+'.pickle', 'wb') as handle:
           pickle.dump(trial_hash, handle)
         # reset count and dictionary!
         trial_cnt = 0
         trial_hash = {}

      # record the mothid, trial count, and trial length in a log file
      # --(!) Logging must be done after we determine whether this set
      # of trials is for a new moth.
      if (trial_cnt == 0):
         writeToFile(logfile,str(new_moth)+":")
      writeToFile(logfile,"\tt"+str(trial_cnt)+" = "+str(len(raw_data.values)))

      # process x,y,hx,hy slice of raw data into the dictionary of discretized frames
      traj = raw_data[['pos_x','pos_y','head_x', 'head_y']]
      trial_datetime = raw_data.datetime.iloc[0]
      discretize_and_save(trial_hash,forest,traj,'t'+str(trial_cnt),trial_datetime)
      # update the current mothid
      mothname = new_moth
      # update trial count
      trial_cnt += 1

   # save the last trial into trial dictionary
   print(mothname+": saving "+str(trial_cnt)+" trajs in "+filepath+'/'+desc+".pickle")
   with open(filepath+'/'+desc+'.pickle', 'wb') as handle:
     pickle.dump(trial_hash, handle)

   return

def main():
   DATA_LOC = "../data/masks/original_set"
   FOREST_LOC = "../data/forests/forest.csv"
   import sys
   # if a new forest path is specified, then save masks as a random set
   if (len(sys.argv) == 2):
      FOREST_LOC = sys.argv[1]
      DATA_LOC = DATA_LOC.replace('original_set','random_sets')
      DATA_LOC += "/"+FOREST_LOC.split('/')[-1]
      # make sure directory exists for saving data
      if not os.path.exists(DATA_LOC):
         os.makedirs(DATA_LOC)

   """ LOAD & INITIALIZE DATA """
   # read tree data
   forest = load_dataframe("csv",FOREST_LOC)
   print( "Forest size: "+str(len(forest.values)) )

   # terminate early if forest data is empty
   if(len(forest) == 0):
      print("(!) ERROR: No tree data loaded.")
      return

   # prepare to log processed trials in Notes file and record datetime
   if (os.path.exists(DATA_LOC+"/trial_log")):
      LOG = open(DATA_LOC+"/trial_log",'ab') # append to file
   else:
      LOG = open(DATA_LOC+"/trial_log",'wb')
   import time,datetime
   writeToFile(LOG,str(datetime.datetime.fromtimestamp(time.time())))

   # gather single trial data stored in hdf format
   single_trials = glob.glob("/home/bilkit/Dropbox/moth_nav_analysis/data/single_trials/*.h5")
   if (len(single_trials) < 1):
      print("No trials to process.\n~~Done.")
      return
   single_trials.sort()
   print("Computing masks for:")
   # print file names that will be processed
   for t in single_trials: print('\t'+t+'\n')
   # start processing trial data
   processTrials(single_trials,forest,DATA_LOC,LOG)

   # cleanup files
   LOG.close()


   print("~~Done :)")
   return

main()


