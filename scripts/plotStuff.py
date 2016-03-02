#!/usr/bin/python3

import matplotlib.pyplot as plt
import matplotlib.patches as patches

# displays plot if no filename is
# specified otherwise save plot
# using file arg
# ARGS: plot, filename
# RETURNS: void
def visualize(plt,filename):
   if(filename == None):
      plt.show()
   else:
      plt.savefig(filename)

   plt.close();
   return

# displays plot of non-zero values
# in matrix where each index represents
# a block of size bsz. Please pass a
# sparse matrix.
# ARGS: matrix (sparse), block size,
#   filename (optional)
# RETURNS: void
def plot_mat(mat,bsz,targ_file=None):
   ax = plt.figure().add_subplot(111)
   ax.set_axis_bgcolor('black');

   # get matrix shape
   szx = mat.shape[0]
   szy = mat.shape[1]

   print("plotting mat("+str(szx)+"x"+str(szy)+")")
   for row in range(0,szx):
      for col in range(0,szy):
         if mat[row][col] != 0:
            if mat[row][col] < 0:
               ax.scatter(row,col,s=bsz*100,c='b',marker='x')
            else:
               ax.scatter(row,col,s=bsz*100,c='r',marker='x')

   plt.title("kernel (block_size="+str(round(bsz,5))
      +" ksize="+str(round(bsz*szx,5))+")")
   plt.xlabel("discritized x")
   plt.xlim(-1,szx)
   plt.ylabel("discritized y")
   plt.ylim(-1,szy)

   visualize(plt,targ_file)
   return

# displays objects in environment and
# trajectory path. Pass a filename to
# save the figure.
# ARGS: trajectory, environment, file (opt)
# RETURNS: void
def plot(traj,env,targ_file=None):
   ax = plt.figure().add_subplot(111)

   print("plotting trees: "+str(len(env)))
   for tree in env.values:
      ax.add_patch(plt.Circle((tree[0],tree[1]),tree[2],color='g'))

   print("plotting pts: "+str(len(traj)))
   ax.scatter(traj.pos_x,traj.pos_y,s=5,c='b',marker='.')

   if('obstacles' in traj.columns):
      plt.title(traj.moth_id.iloc[0]+" in "+traj.obstacles.iloc[0]+" forest")
   else:
      plt.title(traj.moth_id.iloc[0]+" in bright forest")
   plt.xlabel("x")
   plt.xlim(
      min(min(env.x),min(traj.pos_x)),
      max(max(env.x),max(traj.pos_x)))
   plt.ylabel("y")
   plt.ylim(
      min(min(env.y),min(traj.pos_y)),
      max(max(env.y),max(traj.pos_y)))

   visualize(plt,targ_file)
   return

# displays objects in environment, patch,
# and trajectory point. A box of length
# 2*patch size is drawn to visually indicate
# patch boundary. Pass a filename to save
# the figure.
# ARGS: point, patch, patch size, env
#  filename (opt)
# RETURNS: void
def plot_frame(pt,patch,size,env,targ_file=None):
   ax = plt.figure().add_subplot(111)

   print("plotting trees: "+str(len(env)))
   # plot trees outside of patch
   for tree in env.values:
      if(not(tree[0] in patch.x and tree[1] in patch.y and tree[2] in patch.r)):
         ax.add_patch(plt.Circle((tree[0],tree[1]),tree[2],color='g'))

   print("plotting patch trees: "+str(len(patch)))
   ax.scatter(pt.pos_x,pt.pos_y,s=100*max(env.r),c='b',marker='x')
   # plot trees in patch
   for tree in patch.values:
      ax.add_patch(plt.Circle((tree[0],tree[1]),tree[2],color='c'))
   # draw boundary of patch in case no trees are in it
   xoffset = pt.pos_x-size
   yoffset = pt.pos_y-size
   ax.add_patch(patches.Rectangle(
      (xoffset,yoffset)
      ,2*size
      ,2*size
      ,fill=False
      ,edgecolor="red"))

   plt.title("scoring window centered on moth (patch dim="
      +str(2*size)+'x'+str(2*size)+")")
   plt.xlabel("x")
   plt.xlim(
      min(min(env.x),pt.pos_x),
      max(max(env.x),pt.pos_x))
   plt.ylabel("y")
   plt.ylim(
      min(min(env.y),pt.pos_y),
      max(max(env.y),pt.pos_y))

   visualize(plt,targ_file)
   return