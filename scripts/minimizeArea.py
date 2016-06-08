#!/usr/python2.7

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
import numpy
import math

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

# Initialize problem input and output vectors

NPOINTS = 3
POINT_RANGE = (-10,10)
MSQUARES = 1
# later, we generate a set of N points of size SETS
SETS = 10
# input : [(p0x,p0y),...,(pNx,pNy)]
inputs = [[(0,0) for i in range(NPOINTS)]] * SETS
# output : [S0,...,SM] where S = (xleft,ybottom,length)
outputs = [[None]] * SETS

# (TODO) initialize input and output
for i in range(SETS):
  # input - select random x and y using (max - min) range
  # then shift x and y by min (i.e., x+min, y+min)

  # output - write a script that finds min area using
  # some extant algorithm.
  # This step is unclear because there is no straight
  # forward way to verify the potential solutions like
  # the mux.py example demos.

  if(i == SETS-1): print("init completed")

pset = gp.PrimitiveSet("MAIN", MUX_TOTAL_LINES, "IN")
# (TODO) add terminals and primitives
# operations:
# - insert unit square to the set of squares *this op allows us to
#   add in a new set of parameters that contribute to a potentially
#   higher scoring solution.
# - scale a square within the set of squares
# - shift a square within the set of squares
# - if/else or for loop that performs one of
#   the other operations based on whether
#   all points are covered by the current
#   set of squares.
pset.addPrimitive(if_then_else, 3)

# (?) we may need to play around with the weights here
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
# (?) later, experiment with primitive tree min/max height
toolbox.register("expr", gp.genFull, pset=pset, min_=2, max_=4)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

def evaluateMinArea(individual):
  func = toolbox.compile(expr=individual)
  return sum(func(*in_) == out for in_, out in zip(inputs, outputs)),

toolbox.register("evaluate", evaluateMinArea)
toolbox.register("select", tools.selTournament, tournsize=7)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genGrow, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

def main():
  random.seed(10)
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
