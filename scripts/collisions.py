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
   # for tn in env.values:
   #    ax.add_patch(plt.Circle((tn[0],tn[1]),tn[2],color='g'))

   for pn in points.values:
      l_cutoff = env.x > pn[0]-2*Rmax
      r_cutoff = env.x < pn[0]+2*Rmax
      u_cutoff = env.y < pn[1]+2*Rmax
      b_cutoff = env.y > pn[1]-2*Rmax

      tclose = env[l_cutoff & r_cutoff & u_cutoff & b_cutoff]
      if len(tclose) > 0:
         print("tclose: "+str(len(tclose)))
         print("p: ("+str(pn[0])+','+str(pn[1])+')')

      # detect a collision within patch bruh

      for tn in tclose.index:
         if tn in undrawn_trees:
            ax.add_patch(plt.Circle((tclose[tn][0]
               ,tclose.iloc[tn][1])
               ,tclose.iloc[tn][2]
               ,color='r'))
            undrawn_trees.delete(tn)
      print(len(undrawn_trees))

         # no possible collision
      ax.add_patch(plt.Circle((pn[0],pn[1]),.2,color='b'))

   plt.xlim(min(env.x),max(env.x))
   plt.ylim(min(env.y),max(env.y))
   plt.show()

   return