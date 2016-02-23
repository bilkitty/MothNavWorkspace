#!/usr/bin/python3

from plotTrials import plot_frame

# generate score for single traj point

# args:
# traj point
# tree patch (floor(x2) - floor(x1))
# smallest tree rad

# return:
# integer value for traj point

# steps:
# generate MxM mask of trees where M = dx/(Rmin/2)
# generate some kernel MxM
# dot the mask and kernel

# sets up test data and provides visualization
# by default
def setup_test(md,td,visual=True):
   # get a single point
   xypoint = md.loc[0] #(int)((len(md)-1)/2)] # midpoint
   xy = xypoint[['pos_x','pos_y']]

   # get patch around single point
   patch_size = 50*max(td.r)/2
   l = xy[0]-patch_size < td.x+td.r
   r = td.x-td.r < xy[0]+patch_size
   u = td.y-td.r < xy[1]+patch_size
   d = xy[1]-patch_size < td.y+td.r
   patch = td[l & r & u & d]
   # visualize patch
   if(visual):
      plot_frame(xypoint,patch,2*patch_size,td)

   return [xy,patch,patch_size]
