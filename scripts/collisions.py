#!/usr/bin/python3

import pandas as pd
from matplotlib import pyplot as plt

PATCH_SIZE = 20; # search_space (in Rmax units)
R_CLOSECALL = 10; # distance (in Rmax units) from tree edge
                 # and moth edge that counts as close call
#MOTH_RAD = 0; # moth radius is negl. small compared to tree rad

# returns count of close calls and collisions per point
def analyse_patch(pm,patch,rmax,ax):
   collision = 0;
   close = 0;

   for tn in patch.values:
      # compute distance between moth center and tree center
      dd = (tn[0] - pm[0])**2 + (tn[1] - pm[1])**2
      dd = dd**0.5

      # test for collision or close call
      if dd < R_CLOSECALL*rmax:
         if dd < tn[2]:
            collision +=1
      #-- DEBUG
            ax.add_patch(plt.Circle((tn[0]
               ,tn[1])
               ,5
               ,color='r'))
      #-- DEBUG
         else:
            close +=1

   return [close,collision]

# walks along trajectory accumulating collision
# count and close callcount (later score)
def count_collisions_closecalls(traj,env):
   print("INFO: detecting close calls within "+str(PATCH_SIZE)+"*Rmax of traj pt")

   # determines size of patch (aka search space)
   Rmax = max(env.r)
   # keep close call and collision count
   total_count = [0,0]
   # initialize dict of tree indices and binary value
   # representing whether it has been drawn
   undrawn_trees = {}
   for ii in env.index:
      undrawn_trees[ii] = 1
   # isolate (x,y) and <hx,hy> info from traj data
   points = traj[['pos_x','pos_y','head_x','head_y']]

   #-- DEBUG
   ax = plt.figure().add_subplot(111)
   #-- DEBUG

   for pn in points.values:
      # define patch
      l_cutoff = env.x > pn[0]-PATCH_SIZE*Rmax
      r_cutoff = env.x < pn[0]+PATCH_SIZE*Rmax
      u_cutoff = env.y < pn[1]+PATCH_SIZE*Rmax
      b_cutoff = env.y > pn[1]-PATCH_SIZE*Rmax

      # get trees within patch
      tclose = env[l_cutoff & r_cutoff & u_cutoff & b_cutoff]
      #-- DEBUG
      # draw trees within patch bruh
      for tn in tclose.index:
         # print("drawing close trees...")
         if undrawn_trees[tn] == 1:
            ax.add_patch(plt.Circle((env.loc[tn][0]
               ,env.loc[tn][1])
               ,env.loc[tn][2]
               ,color='c'))
            undrawn_trees[tn] = 0

      # draw traj point
      ax.add_patch(plt.Circle((pn[0],pn[1]),.05,color='b'))
      # -- DEBUG

      # check for close call or collision
      count = analyse_patch(pn,tclose,Rmax,ax)
      total_count[0] += count[0]
      total_count[1] += count[1]


   print("closecalls: "+str(total_count[0])+" collisions: "+str(total_count[1]))
#-- DEBUG
   # draw remaining trees
   for tn in undrawn_trees.keys():
      if(undrawn_trees[tn] == 1):
         ax.add_patch(plt.Circle((env.loc[tn][0]
            ,env.loc[tn][1])
            ,env.loc[tn][2]
            ,color='g'))
         undrawn_trees[tn] = 0

   plt.xlim(min(min(env.x),min(traj['pos_x']))
      ,max(max(env.x),max(traj['pos_x'])))
   plt.ylim(min(min(env.y),min(traj['pos_y']))
      ,max(max(env.y),max(traj['pos_y'])))
   # plt.show()

   # prompt to save figure
   yes_or_no = input("save figure? (yes/no)\n")
   if(yes_or_no.lower() == "yes"):
      target_file = input("filename: ")
      plt.savefig(target_file)
#-- DEBUG

   return