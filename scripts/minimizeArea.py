#!/usr/bin/python2.7

"""
This script implements a toy problem that we will use to
roughly understand how deap works. The problem involves
covering a set of points with some set of squares of minimal
area. The squares are defined by a point (x,y) describing
the bottom-left corner and a length. The individual squares
can be shifted and scaled, and the set of squares can grow.
We attempt to use deap's genetic programming framework to
find an optimal solution to this problem.
"""

import operator
import random
import numpy
import math

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

# run one of two functions based on condition
def if_then_else(condition, out1, out2):
  """
  (bool, functools.partial, functools.partial) -> None
  """
  out1() if condition else out2()
  return

# define a class describing the problem
# members:
#   --input data--
#   set of points ([[double,double]])
#   --properties--
#   iscovered ([bool])(indices correspond to points in set of points)
#   total area (int)
#   --output data--
#   set of squares ([[double,double,int]])
# methods:
#   --validationMethods--
#   covers_point() -> bool
#   --modificationMethods--
#   insertSquare(pointSelectionMethod) -> None
#   scaleSquare(squareSelectionMethod, scalar) -> None
#   --selectionMethods--
#   randomPoint() -> [double,double]
#   minPoint() -> [double,double]
#   randomSquare() -> int
#   minSquare() -> int
#   randomScale() -> int
#   --outputGeneration--
#   buildSet() -> None
def insert_unit_square(squares,xy):
  """
  ([[double,double,int]],[double,double]) -> [[double,double,int]]
  """
  if (squares == None):
    raise Exception("(!) insert_unit_square: squares is type 'None'.")
  squares.append([xy[0],xy[1],1])
  return squares
def scale_square(squares,index,scalar):
  """
  ([[double,double,int]],int,int) -> [[double,double,int]]
  """
  if (scalar <= 0):
    raise Exception("(!) scale_square: scalar <= 0.")
  # only apply scalar to valid index
  if (0 <= index and index < len(squares)):
    squares[index][2] *= scalar
  return squares
def shift_square(squares,index,dxdy):
  """
  ([[double,double,int]],int,[double,double]) -> [[double,double,int]]
  Shift the square at the given index by dxdy and return the modified set
  of squares. dxdy is the difference in x and y between the source point
  and destination. In other words, if the source locaiton is [a,b] and the
  destination is [c,d] then dxdy is [a-c,b-d].
  """
  # only apply shift to valid index
  if (0 <= index and index < len(squares)):
    squares[index][0] -= dxdy[0]
    squares[index][1] -= dxdy[1]
  return squares

# Initialize problem input and output vectors
NPOINTS = 3
POINT_RANGE = (-10,10)
MAX_SQUARES = sum(numpy.ceil(numpy.abs(POINT_RANGE)))**2
# later, we generate a set of N points of size SETS
SETS = 10
# input : [[p0x,p0y],...,[pNx,pNy]]
inputs = [[None]] * SETS
# output : [S0,...,SM] where S = [xleft,ybottom,length]
# outputs = [[None]] * SETS

# initialize input and output
random.seed(10)
# Generates two random numbers in the range; including endpoints.
# ((int,int)) -> ([double,double])
randomXY = lambda rangeXY: [random.uniform(rangeXY[0],rangeXY[1]),random.uniform(rangeXY[0],rangeXY[1])]
# potential fitness functions - a lower score from these functions is better

for i in range(SETS):
  # input - select random x and y in point range
  inputs[i] = [randomXY(POINT_RANGE) for j in range(NPOINTS)]
  print ("INPUT:")#, end="\t")
  print (inputs[i])

  # output - no need to generate an optimal solution for comparison.
  # Instead, we use the ratio between points covered and total area vs. 1.
  # outputs[i] = [[inputs[i][j][0],inputs[i][j][1],1] for j in range(NPOINTS)]
  # print ("OUTPUT:")#, end="\t")
  # print (outputs[i])

  if(i == SETS-1): print ("init completed")

import itertools
# (!) PrimitiveSetTyped cannot accept nest lists or itertools.repeat
input_types = itertools.repeat(list,NPOINTS) # expect [[float,float]]*NPOINTS
# output_types = itertools.repeat(list,SETS) # expect [[float,float,int]]*variablesize

pset = gp.PrimitiveSetTyped("MAIN"
  , input_types
  , None #output_types
  , "IN")

# (TODO) add terminals and primitives TYPED
# operations:
def somefunc(alist):
  return alist
pset.addPrimitive(somefunc, [list,list], list)
# terminals:
# pset.addTerminal()

# pset.addPrimitive(if_then_else, 3)

# (?) we may need to play around with the weights here
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
# (?) later, experiment with primitive tree min/max height
toolbox.register("expr", gp.genFull, pset=pset, min_=2, max_=4)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

# (TODO) The following may make good fitness functions:
# - points covered / total area >= 1 is a good score. If a solution breaks this threshold, stop.
def evaluateMinArea(individual):
  func = toolbox.compile(expr=individual)
  # accumulate the absolute differences between output from compiled individual with worstcase output
  return

toolbox.register("evaluate", evaluateMinArea)
toolbox.register("select", tools.selTournament, tournsize=7)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genGrow, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

def main():

  pop = toolbox.population(n=40)
  hof = tools.HallOfFame(1)
  stats = tools.Statistics(lambda ind: ind.fitness.values)
  stats.register("avg", numpy.mean)
  stats.register("std", numpy.std)
  stats.register("min", numpy.min)
  stats.register("max", numpy.max)

  algorithms.eaSimple(pop, toolbox, 0.8, 0.1, 40, stats,halloffame=hof,verbose=True)

  return pop, stats, hof

if __name__ == "__main__":
  main()
