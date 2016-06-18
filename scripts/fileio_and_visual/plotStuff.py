#!/usr/bin/python3

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# displays plot if no filename is
# specified otherwise save plot
# using file arg
# ARGS: plot, filename
# RETURNS: void
def visualize(filename):
   if(filename == None):
      plt.show()
   else:
      plt.savefig(filename)

   plt.close()
   return

def init_axes(bgcolor="black"):
   """
   (None) -> matplotlib.axes.AxesSubplot
   """
   fig = plt.figure()
   ax = fig.add_subplot(111)
   ax.set_axis_bgcolor(bgcolor)
   return ax

def plot_scores(scores,mid,tn,targ_file=None):
   ax = init_axes()
   n = len(scores)
   # bar chart parameters
   bar_idx = np.arange(n)
   bar_width = 0.1
   # use 10% of score range as pad
   pad = 0.1*(max(scores) - min(scores))

   # plot bars using alternating colors
   even_frames = [scores[i] for i in range(0,n,2)]
   odd_frames = [scores[i] for i in range(1,n,2)]

   ax.bar(bar_idx[0::2], even_frames, color='c')
   ax.bar(bar_idx[1::2], odd_frames, color='y')

   plt.title("scores for "+mid+" t"+str(tn))
   plt.xlabel("trajectory frame")
   plt.xlim(-1,n+1)
   plt.ylabel("score")
   plt.ylim(min(scores)-pad,max(scores)+pad+1)

   visualize(targ_file)

   return

# displays plot of non-zero values
# in matrix where each index represents
# a block of size bsz. Please pass a
# sparse matrix.
# ARGS: matrix (sparse), block size,
#   filename (optional)
# RETURNS: void
def plot_mat(mat,bsz,kern=None,targ_file=None):
   ax = init_axes()

   # get matrix shape
   szx = mat.shape[0]
   szy = mat.shape[1]
   mark_size = bsz*100

   if kern == None:
      kern = np.ones((szx,szy),dtype=int)

   print("plotting mat("+str(szx)+"x"+str(szy)+")")
   for row in range(0,szx):
      for col in range(0,szy):
         # show centers of moth/trees
         if mat[row][col] < 0:
            ax.scatter(row,col,s=mark_size*kern[row][col],c='b',marker='x')
         elif mat[row][col] > 0:
            ax.scatter(row,col,s=mark_size*kern[row][col],c='r',marker='x')
         else:
            continue


   plt.title("matrix (block_size="+str(round(bsz,5))
      +" msize="+str(round(bsz*szx,5))+")")
   plt.xlabel("discritized x")
   plt.xlim(-1,szx)
   plt.ylabel("discritized y")
   plt.ylim(-1,szy)

   visualize(targ_file)
   return

def plot_traj(axes,traj,last_plot=True,targ_file=None):
   """
   (matplotlib.axes.AxesSubplot,pandas.dataframe,bool,str) -> None

   Adds a plot of a dataframe (with columns [...,'pos_x','pos_y',...]) to the
   subplot, axes. If last_plot is False, then the plot is not visualized. If
   a target file is specified, then the plot is saved as targ_file.

   >>> from fileio import load_dataframe
   >>> import os, sys
   >>> traj = load_dataframe("h5",os.getcwd()+"/test/moth1_448f0.h5")
   loading: /home/bilkit/Dropbox/moth_nav_analysis/scripts/test/moth1_448f0.h5
   >>> ax = init_axes("white")
   >>> plot_traj(ax,traj)
   plotting pts: 3454
   >>> ax = init_axes()
   >>> plot_traj(ax,traj,last_plot=False)
   plotting pts: 3454
   >>> sys.stdout = plt.xlabel("x")
   >>> sys.stdout = plt.xlim(min(traj.pos_x),max(traj.pos_x))
   >>> sys.stdout = plt.ylabel("y")
   >>> sys.stdout = plt.ylim(min(traj.pos_y),max(traj.pos_y))
   >>> visualize(os.getcwd()+"/test/traj.png")
   """
   print("plotting pts: "+str(len(traj)))
   axes.scatter(traj.pos_x,traj.pos_y,s=5,c='r',marker='.')

   if('obstacles' in traj.columns):
      plt.title(traj.moth_id.iloc[0]+" in "+traj.obstacles.iloc[0]+" forest")
   else:
      plt.title(traj.moth_id.iloc[0]+" in bright forest")

   # save or display the plot if it is last
   if (last_plot):
      plt.xlabel("x")
      plt.xlim(min(traj.pos_x),max(traj.pos_x))
      plt.ylabel("y")
      plt.ylim(min(traj.pos_y),max(traj.pos_y))
      visualize(targ_file)

   return

def plot_trees(axes,trees,last_plot=True,targ_file=None):
   """
   (matplotlib.axes.AxesSubplot,pandas.dataframe,bool,str) -> None

   Adds a plot of a dataframe (with columns ['x', 'y', 'r']) to the add_subplot,
   axes. If last_plot is False, then the plot is not visualized. If a target
   file is specified, then the plot is saved as targ_file.

   >>> from fileio import load_dataframe
   >>> import os, sys
   >>> trees = load_dataframe("csv",os.getcwd()+"/test/trees.csv")
   loading: /home/bilkit/Dropbox/moth_nav_analysis/scripts/test/trees.csv
   >>> ax = init_axes()
   >>> plot_trees(ax,trees)
   plotting trees: 1000
   >>> ax = init_axes()
   >>> plot_trees(ax,trees,last_plot=False)
   plotting trees: 1000
   >>> sys.stdout = plt.xlabel("x")
   >>> sys.stdout = plt.xlim(min(trees.x),max(trees.x))
   >>> sys.stdout = plt.ylabel("y")
   >>> sys.stdout = plt.ylim(min(trees.y),max(trees.y))
   >>> visualize(os.getcwd()+"/test/trees.png")
   """
   print("plotting trees: "+str(len(trees)))
   for tree in trees.values:
      axes.add_patch(plt.Circle((tree[0],tree[1]),tree[2],color='g'))

   # save or display the plot if it is last
   if (last_plot):
      plt.xlabel("x")
      plt.xlim(min(trees.x),max(trees.x))
      plt.ylabel("y")
      plt.ylim(min(trees.y),max(trees.y))
      visualize(targ_file)
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
   ax = init_axes()

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

   visualize(targ_file)
   return

""" DOC TESTS """
if __name__ == "__main__":
   import doctest
   doctest.testmod()
