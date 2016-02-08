#!/usr/bin/python3

import matplotlib.pyplot as plt

def plot(traj,env,targ_file):
   # pts = traj[['pos_x','pos_y']][:]
   # # won't plot because of index?
   # pts.plot(kind = 'scatter');

   ax = plt.figure().add_subplot(111)

   print("plottig pts: "+str(len(traj)))
   ax.scatter(traj.pos_x,traj.pos_y,s=5,c='b',marker='.')

   print("plottig trees: "+str(len(env)))
   # save tree in header
   # ax.add_patch(plt.Circle((int(float(env.columns[0]))
   #    ,int(float(env.columns[1])))
   #    ,int(float(env.columns[2]))
   #    ,color='g'))
   # env.columns = ['pos_x','pos_y','radius']
   for tree in env.values:
      ax.add_patch(plt.Circle((tree[0],tree[1]),tree[2],color='g'))

   plt.title(traj.moth_id.iloc[0]+" in "+traj.obstacles.iloc[0]+" forest")
   plt.xlabel("x")
   plt.xlim(min(min(env.pos_x),min(traj.pos_x)),max(max(env.pos_x),max(traj.pos_x)))
   plt.ylabel("y")
   plt.ylim(min(min(env.pos_y),min(traj.pos_y)),max(max(env.pos_y),max(traj.pos_y)))

   plt.savefig(targ_file)
   return
