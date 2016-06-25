#!/bin/bash

# HOW TO RUN:
# $ source configure_python_environment.bash

# This script appends script sub-directories to the PYTHONPATH env
# variable. The path needs to be configured so that pyscripts can
# reference those that are contained in sub-directories.

scripts_dir=`pwd`
export PYTHONPATH=$PYTHONPATH:"$scripts_dir"/fileio_and_visual:"$scripts_dir"/preprocess_trajs:"$scripts_dir"/score_trajs
echo PYTHONPATH=$PYTHONPATH