#!/usr/bin/python3

import pandas as pd   # data handling
import matplotlib.pyplot as plt
import os.path as osp # file exists
import sys            # commandline args

weird_moth = 'moth5_inc'
DEBUG = True

def plot(traj,env,targ_file):
   ax = plt.figure().add_subplot(111)

   print("plottig pts: "+str(len(traj)))
   # ax.scatter(traj.pos_x,traj.pos_y,s=5,c='b',marker='.')

   print("plottig trees: "+str(len(env)))
   ax.scatter(env.pos_x,env.pos_y,s=10,c='g',marker='o')

   plt.title(traj.moth_id.iloc[0]+" in "+traj.obstacles.iloc[0]+" forest")
   plt.xlabel("x")
   plt.ylabel("y")


   plt.savefig(targ_file)
   return

# returns list of trajectories and trajectory count
def get_trajs(data,obst,speed,fmin,fmax,mid):
   # tree data has no obstacle field
   if('obstacles' in data.columns):
      obs_slice = sel_obstacle(data,obst)
   else:
      obs_slice = data

   moth_slice = sel_moth(sel_fmax(sel_fmin(sel_speed(obs_slice
      ,speed)
      ,fmin)
      ,fmax)
      ,mid)

   return moth_slice

def sel_moth(block,name):
   return block.loc[block.moth_id == name]

def sel_obstacle(block,name):
   return block.loc[block.obstacles == name]

def sel_speed(block,val):
   return block.loc[block.flight_speed == val]

def sel_fmin(block,val):
   return block.loc[block.fog_min == val]

def sel_fmax(block,val):
   return block.loc[block.fog_max == val]

# returns NULL if failed to load file
def load_data(type,fpath):
   if(not osp.isfile(fpath)):
      print("(!) ERROR: "+fpath+" does not exist.")
      return None

   if(type == 'csv'):
      dt = pd.read_csv(fpath,delimiter=',')
   elif(type == 'h5'):
      # get name of data set by file name
      fname = fpath.split('/')[-1]
      dt = pd.read_hdf(fpath,fname.split('.')[0])
   else:
      print("(!) ERROR: file type, "+type+", is unrecognized.")
      dt = None

   return dt

# plot some data

def main():
   argc = len(sys.argv)
   if(argc == 3):
      path_to_data = sys.argv[1]
      plot_output = sys.argv[2]
   else:
      print("(!) ERROR: Invalid args, see usage.\nUsage: ./plot_moth_data path_to_data")
      return
   # trim '/' off path
   end = len(path_to_data)-1
   if(path_to_data[end] == '/'):
      path_to_data = path_to_data[:end]

   # read moth and tree data
   dtree = load_data('csv',path_to_data+'/bright_trees.csv') # 12 labels (no obst)
   dmoth = load_data('h5',path_to_data+'/moth_data.h5') # 13 labels
   # check for loaded files
   # if(not dtrial):
   #    return

   # test plot all of moth_n
   tt = get_trajs(dmoth,'bright',4.0,4.0,8.0,'moth2')
   trees = get_trajs(dtree,'bright',4.0,4.0,8.0,'moth2')
   # check that tt is not empty
   # check that tree is not emtpy
   plot(tt,trees,plot_output)

   print("~~Done :)")
   return

main()