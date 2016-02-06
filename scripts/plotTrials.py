#!/usr/bin/python3

import pandas as pd   # data handling
import matplotlib.pyplot as plt
import os.path as osp # file exists
import sys            # commandline args

weird_moth = 'moth5_inc'
DEBUG = True


def plot(traj,env,targ_file):
   # pts = traj[['pos_x','pos_y']][:]
   # # won't plot because of index?
   # pts.plot(kind = 'scatter');

   # zoom to fit trees & traj
   # min/max of points


   ax = plt.figure().add_subplot(111)

   print("plottig pts: "+str(len(traj)))
   ax.scatter(traj.pos_x,traj.pos_y,s=5,c='b',marker='.')

   print("plottig trees: "+str(len(env)))
   # save tree in header
   ax.add_patch(plt.Circle((int(float(env.columns[0]))
      ,int(float(env.columns[1])))
      ,int(float(env.columns[2]))
      ,color='g'))
   env.columns = ['pos_x','pos_y','radius']
   for tree in env.values:
      ax.add_patch(plt.Circle((tree[0],tree[1]),tree[2],color='g'))

   plt.title(traj.moth_id.iloc[0]+" in "+traj.obstacles.iloc[0]+" forest")
   plt.xlabel("x")
   plt.xlim(min(min(env.pos_x),min(traj.pos_x)),max(max(env.pos_x),max(traj.pos_x)))
   plt.ylabel("y")
   plt.ylim(min(min(env.pos_y),min(traj.pos_y)),max(max(env.pos_y),max(traj.pos_y)))

   plt.savefig(targ_file)
   return

# returns dictionary of trajectories by start and end indecies
# key = 't'+n, value = [range1,range2]
def get_trajs(data,obst,speed,fmin,fmax,mid):
   # tree data has no obstacle field
   if('obstacles' in data.columns):
      obs_slice = data[sel_obstacle(data,obst)]
   else:
      obs_slice = data.copy(False)

   moth_slice = obs_slice[sel_speed(data,speed)
         & sel_fmin(data,fmin)
         & sel_fmax(data,fmax)
         & sel_moth(data,mid)]

   # extract however many trials exist in moth set
   dd = {}
   iit = 0
   flight = 'f'
   iprev = moth_slice.index[0]
   start_new = False
   dd[flight+str(iit)] = [iprev,0]

   # save curr index as start of next trial
   # when indices differ by > 1
   # save prev index as end of curr trial
   for ii in moth_slice.index[1:]:
      if (ii - iprev) > 1:
         dd[flight+str(iit)][1] = iprev
         print("flight"+str(iit)+" : "+str(ii)+" - "+str(iprev))
         iit += 1
         dd[flight+str(iit)] = [ii,0]
      # update
      iprev = ii

   # include last index
   dd[flight+str(iit)][1] = moth_slice.index[-1]

   #--DEBUG
   # verify extraction by checking length
   tlen=0
   for el in dd.values():
       tlen += len(data[el[0]:el[1]])

   if(tlen != len(moth_slice)):
      print("tlen: "+str(tlen))
      print("ms: "+str(len(moth_slice)))
      print("failed to obtain trajs")

   return dd

def sel_moth(block,name):
   return block.moth_id == name

def sel_obstacle(block,name):
   return block.obstacles == name

def sel_speed(block,val):
   return block.flight_speed == val

def sel_fmin(block,val):
   return block.fog_min == val

def sel_fmax(block,val):
   return block.fog_max == val

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
      print("(!) ERROR: Invalid args, see usage.\nUsage: ./plot_moth_data path_to_data output.png")
      return
   # trim '/' off path
   end = len(path_to_data)-1
   if(path_to_data[end] == '/'):
      path_to_data = path_to_data[:end]

   # read moth and tree data
   dtree = load_data("csv","/media/usb/data_working/forest_sans_header.csv") # 12 labels (no obst)
   dmoth = load_data("h5",path_to_data+"/moth_data.h5") # 13 labels
   # check for loaded files
   # if(not dtrial):
   #    return

   # test plot all of moth_n
   trajs = get_trajs(dmoth,'bright',4.0,4.0,8.0,weird_moth)
   tt = dmoth[trajs['f0'][0]:trajs['f0'][1]]

   # check that tt is not empty
   # check that tree is not emtpy
   plot(tt,dtree,plot_output)

   print("~~Done :)")
   return

main()