#!/usr/bin/python3

import matplotlib.pyplot as plt
import matplotlib.patches as patches

def plot(traj,env,targ_file):
   ax = plt.figure().add_subplot(111)

   print("plottig trees: "+str(len(env)))
   for tree in env.values:
      ax.add_patch(plt.Circle((tree[0],tree[1]),tree[2],color='g'))

   print("plottig pts: "+str(len(traj)))
   ax.scatter(traj.pos_x,traj.pos_y,s=5,c='b',marker='.')

   if('obstacles' in traj.columns):
      plt.title(traj.moth_id.iloc[0]+" in "+traj.obstacles.iloc[0]+" forest")
   else:
      plt.title(traj.moth_id.iloc[0]+" in bright forest")
   plt.xlabel("x")
   plt.xlim(min(min(env.x),min(traj.pos_x)),max(max(env.x),max(traj.pos_x)))
   plt.ylabel("y")
   plt.ylim(min(min(env.y),min(traj.pos_y)),max(max(env.y),max(traj.pos_y)))

   if(targ_file == None):
      plt.show()
   else:
      plt.savefig(targ_file)

   plt.close();
   return

def plot_frame(pt,patch,size,env):
   ax = plt.figure().add_subplot(111)

   print("plotting trees: "+str(len(env)))
   for tree in env.values:
      if(not(tree[0] in patch.x and tree[1] in patch.y and tree[2] in patch.r)):
         ax.add_patch(plt.Circle((tree[0],tree[1]),tree[2],color='g'))

   print("plotting point and patch: "+str(len(patch)))
   ax.scatter(pt.pos_x,pt.pos_y,s=100*max(env.r),c='b',marker='x')
   for tree in patch.values:
      ax.add_patch(plt.Circle((tree[0],tree[1]),tree[2],color='c'))
   # draw boundary of patch in case no trees are in it
   xoffset = pt.pos_x-(size/2)
   yoffset = pt.pos_y-(size/2)
   ax.add_patch(patches.Rectangle(
      (xoffset,yoffset)
      ,size
      ,size
      ,fill=False
      ,edgecolor="red"))

   plt.title(pt.moth_id+" in bright forest")
   plt.xlabel("x")
   plt.xlim(min(min(env.x),pt.pos_x),max(max(env.x),pt.pos_x))
   plt.ylabel("y")
   plt.ylim(min(min(env.y),pt.pos_y),max(max(env.y),pt.pos_y))

   plt.show()
   plt.close();
   return