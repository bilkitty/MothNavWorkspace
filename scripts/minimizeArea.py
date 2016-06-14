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
import sys

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

"""
Helper functions
"""
# conditionally call one of two functions
def if_then_else(condition, out1, out2):
  """
  (bool, functools.partial, functools.partial) -> None
  """
  out1() if condition else out2()
  return
#   --selectionMethods--
#   randomPoint() -> [double,double]
#   randomScale() -> int
random.seed(10)
# Generates two random numbers in the point range; including endpoints.
# ((int,int)) -> ([double,double])
randomXY = lambda rangeXY: [random.uniform(rangeXY[0],rangeXY[1]),random.uniform(rangeXY[0],rangeXY[1])]
# Generates a random integer within the scalar range; including endpoints.
# ((int,int)) -> (int)
randomScalar = lambda rangeScalar: random.randint(rangeScalar[0],rangeScalar[1])

"""
Problem description:
Given a set of points, find a set of squares that encloses them with
minimal area. The squares are defined by lower-left corner and a size.
The set can be expanded and individual squares can be scaled by integer
values.
"""
# define a class describing the problem
# (!) come up with a good name
class problem(object):
# members:
#   --input data--
#   set of points ([[double,double]])
#   --properties--
#   iscovered ([bool])(indices correspond to points in set of points)
#   total area (int)
#   --output data--
#   set of squares ([[double,double,int]])
  def __init__(self,sets,npoints,max_squares,point_range):
    """
    (int,int,int,[double,double]) -> None
    """
    # init random input bound by point range
    self.sets_of_points = numpy.array([[randomXY(point_range)
      for j in range(npoints)]
      for k in range(sets)],dtype=float)
    # (!) debug
    for i in range(sets):
      print ("INPUT:")
      print (sets_of_points[i])
      if(i == sets-1): print ("init completed")
    # init properties
    self.iset = 0
    self.total_area = 0
    self.isCovered = numpy.zeros(sets_of_points.shape,dtype=bool)
    self.max_squares = max_squares
    # keep track of position within a set at the last index
    self.sets_of_squares = numpy.array([[[0.,0.,0.]]*(max_squares+1)]*sets,dtype=float)


# methods:
#   --validationMethods--
#   covers_point() -> bool
#   --modificationMethods--
#   insertSquare(pointSelectionMethod) -> None
#   scaleSquare(squareSelectionMethod, scalar) -> None
#   nextSet() -> None
  def next_set(self):
    self.iset += 1
    return

  def insert_unit_square(self):
    """
    (None) -> None
    Adds a unit square to the ith set of squares. The location of the square
    can either be random or a point defined by the min(x) and min(y) in the
    set of points.
    """
    last_index = (int) self.sets_of_squares[self.iset][-1][0]
    xy = numpy.array([0,0],dtype=float)
    # choose a random or minimum xy location
    # (?) what should be the deciding factor?

    self.sets_of_squares[self.iset][last_index] = [xy[0],xy[1],1]
    self.sets_of_squares[self.iset][-1][0] += 1
    return

# (!) consider passing the index for a square that can be scaled by scalar
#     to cover a new point. i.e., throw out random/min square.
  def scale_square(self,scalar):
    """
    (int) -> None
    Scales either a random or minimum area square in the ith set of squares
    by scalar.
    """
    index = 0
    # choose a random or minimum area index to scale
    # (?) what should be the deciding factor?

    self.sets_of_squares[self.iset][index][2] *= scalar
    return

  #   --selectionMethods--
  #   minPoint() -> [double,double]
  #   randomSquare() -> int
  #   (!) minSquare() -> int
  # Returns the min x and y from the set of points
  # None -> [double,double]
  minPoint = lambda: [min(points[:,0]),min(points[:,1])]
  # Generates a random integer within range of number of squares; including endpoints.
  # (int) -> (int)
  randomSquareIndex = lambda iset: random.randint(0,len(sets_of_squares[iset])-1)

  def minSquare(self):
    """
    (int) -> (int)
    Returns the index of the smallest square from the set of squares
    (!) keep set of squares as a heap then we don't need this function.
    """
    min_square = 0
    min_area = sys.maxsize
    for i,s in enumerate(self.sets_of_squares[self.iset]):
      if (s[2] < min_area):
        min_square = i
        min_area = s[2]
    return min_square
  #   --outputGeneration--
  #   buildSet() -> None

  # def shift_square(squares,index,dxdy):
  #   """
  #   ([[double,double,int]],int,[double,double]) -> [[double,double,int]]
  #   Shift the square at the given index by dxdy and return the modified set
  #   of squares. dxdy is the difference in x and y between the source point
  #   and destination. In other words, if the source locaiton is [a,b] and the
  #   destination is [c,d] then dxdy is [a-c,b-d].
  #   """
  #   # only apply shift to valid index
  #   if (0 <= index and index < len(squares)):
  #     squares[index][0] -= dxdy[0]
  #     squares[index][1] -= dxdy[1]
  #   return squares

"""
Initialize problem
"""
NPOINTS = 3
POINT_RANGE = (-10,10)
SETS = 10
MAX_SQUARES = sum(numpy.ceil(numpy.abs(POINT_RANGE)))**2

# set up problem; instantiate object
# squareGenerator =

"""
Individual description:
A program that generates a set of squares that may be a solution to the
above problem.
"""
import itertools
# (!) PrimitiveSetTyped cannot accept nest lists or itertools.repeat
input_types = None
output_types = None
pset = gp.PrimitiveSetTyped("MAIN"
  , input_types
  , output_types
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
