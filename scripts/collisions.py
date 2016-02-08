#!/usr/bin/python3

import pandas as pd
from matplotlib import pyplot as plt

BUFF = 1

# returns true if collision occurs
def detect_collision(pmoth,ptree,Rmax):
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
   Rmax = max(env.x)
   points = traj[['pos_x','pos_y','head_x','head_y']]

   #DEBUG
   ax = plt.figure().add_subplot(111)
   for tn in env.values:
      ax.add_patch(plt.Circle((tn[0],tn[1]),tn[2],color='g'))

   for pn in points.values:
      # # pn = pt[0]
      # for tn in env.values:
      #    # tn = tree[0]
      #    # dx = (pn[0]-tn[0])**2
      #    # dy = (pn[1]-tn[1])**2
      #    # if (dx + dy) <= Rmax**2:
      #    # if ((pn[0]-tn[0])**2 + (pn[1]-tn[1])**2) <= Rmax**2:

      #    if( tn[0] < pn[0]+Rmax+BUFF and tn[0] > pn[0]-Rmax-BUFF
      #      and tn[1] < pn[1]+Rmax+BUFF and tn[1] > pn[1]-Rmax-BUFF ):
      #       # detect a collision bruh
      #       ax.add_patch(plt.Circle((tn[0],tn[1]),tn[2],color='r'))
      #       # no possible collision
      ax.add_patch(plt.Circle((pn[0],pn[1]),.2,color='b'))

   plt.xlim(min(env.x),max(env.x))
   plt.ylim(min(env.y),max(env.y))
   plt.show()

   return