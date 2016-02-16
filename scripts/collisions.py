#!/usr/bin/python3

import pandas as pd
from matplotlib import pyplot as plt

# returns true if collision occurs
def detect_collision(pmoth,patch,Rmax):
   #        compute distance = pm - pt
   #        return edge of moth within trad  # sq(D) < sq(trad + mrad)

  return

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
   Rmax = max(env.r)
   points = traj[['pos_x','pos_y','head_x','head_y']]
   undrawn_trees = env.index

   #DEBUG
   ax = plt.figure().add_subplot(111)

   for pn in points.values:
      l_cutoff = env.x > pn[0]-2*Rmax
      r_cutoff = env.x < pn[0]+2*Rmax
      u_cutoff = env.y < pn[1]+2*Rmax
      b_cutoff = env.y > pn[1]-2*Rmax

      tclose = env[l_cutoff & r_cutoff & u_cutoff & b_cutoff]
      if len(tclose) > 0:
         print("p: ("+str(pn[0])+','+str(pn[1])+')')
         print("tclose: "+str(len(tclose)))

      # draw trees within patch bruh
      for tn in tclose.index:
         print("drawing close trees...")
         if tn in undrawn_trees.values:
            ax.add_patch(plt.Circle((tclose.loc[tn][0]
               ,tclose.loc[tn][1])
               ,tclose.loc[tn][2]
               ,color='r'))
            undrawn_trees = undrawn_trees.delete(tn)

      # draw traj point
      ax.add_patch(plt.Circle((pn[0],pn[1]),.05,color='b'))

   # draw remaining trees
   for tn in undrawn_trees.values:
      ax.add_patch(plt.Circle((env.loc[tn][0]
         ,env.loc[tn][1])
         ,env.loc[tn][2]
         ,color='g'))

   plt.xlim(min(env.x),max(env.x))
   plt.ylim(min(env.y),max(env.y))
   plt.show()

   return