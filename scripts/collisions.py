#!/usr/bin/python3

import pandas as pd
from matplotlib import pyplot as plt

PATCH_SIZE = 20; # search_space (in Rmax units)
R_CLOSECALL = 10; # distance (in Rmax units) from tree edge
                 # and moth edge that counts as close call
#MOTH_RAD = 0; # moth radius is negl. small compared to tree rad

# returns count of close calls and collisions per point
def detect_closecalls(pm,patch,rmax,ax):
   # if you drew a line connecting moth and tree
   # consider these points to lie on the line
   # D = d^1/2
   # check D(tc,mc) < R_CLOSECALL
   #   check if collision (i.e. D(tc,mc) <= t_rad)
   #     count collision
   #   else
   #     count close

   collision = 0;
   close = 0;

   for tn in patch.values:
      # compute distance between moth center and tree center
      dd = (tn[0] - pm[0])**2 + (tn[1] - pm[1])**2
      dd = dd**0.5

      if dd < R_CLOSECALL*rmax:
         if dd < tn[2]:
            collision +=1
            ax.add_patch(plt.Circle((tn[0]
               ,tn[1])
               ,5
               ,color='r'))
         else:
            close +=1


   return [close,collision]

# returns count of collisons and close calls
# walks along trajectory accumulating collision
# count and close callcount (later score)
def count_collisions_closecalls(traj,env):
   # get tree radius max
   #Rmax = max(dt.r)
   # get points (x,y,hx,hy)
   #pm11 = m11[['pos_x','pos_y','head_x','head_y']]

   # for all points: # pn = pm11.values[n:n+1][0]
   #   for all trees:
   #     check if inside scope = sq(2*tree radius max)
   #        if( detect_collision ):
   #           count collision
   #        else:
   #           count closecall

   print("INFO: detecting close calls within "+str(PATCH_SIZE)+"*Rmax of traj pt")

   total_score = [0,0]
   Rmax = max(env.r)
   points = traj[['pos_x','pos_y','head_x','head_y']]
   undrawn_trees = env.index

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
      # if len(tclose) > 0:
      #    print("p: ("+str(pn[0])+','+str(pn[1])+')')
      #    print("tclose: "+str(len(tclose)))

      # draw trees within patch bruh
      for tn in tclose.index:
         # print("drawing close trees...")
         if tn in undrawn_trees.values:
            ax.add_patch(plt.Circle((tclose.loc[tn][0]
               ,tclose.loc[tn][1])
               ,tclose.loc[tn][2]
               ,color='g'))
            undrawn_trees = undrawn_trees.delete(tn)

      # draw traj point
      ax.add_patch(plt.Circle((pn[0],pn[1]),.05,color='b'))
      # -- DEBUG

      # check for close call or collision
      score = detect_closecalls(pn,tclose,Rmax,ax)
      total_score[0] += score[0]
      total_score[1] += score[1]


   print("closecalls: "+str(total_score[0])+" collision: "+str(total_score[1]))
#-- DEBUG
   # draw remaining trees
   for tn in undrawn_trees.values:
      ax.add_patch(plt.Circle((env.loc[tn][0]
         ,env.loc[tn][1])
         ,env.loc[tn][2]
         ,color='g'))

   plt.xlim(min(env.x),max(env.x))
   plt.ylim(min(env.y),max(env.y))
   plt.show()
#-- DEBUG

   return