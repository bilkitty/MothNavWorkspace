#!/usr/bin/python3

import pandas as pd
from matplotlib import pyplot as plt

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
