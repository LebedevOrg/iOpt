import math
import unittest
import sys
import numpy as np

from iOpt.problems.rastrigin import Rastrigin
from iOpt.problems.xsquared import XSquared
from iOpt.problems.GKLS import GKLS
from iOpt.solver import Solver
from iOpt.solver_parametrs import SolverParameters
from iOpt.method.listener import StaticPaintListener, AnimationPaintListener, StaticNDPaintListener, AnimationNDPaintListener, ConsoleFullOutputListener

from subprocess import Popen, PIPE, STDOUT


def SolveSingleGKLS():
    """
    Запуск решения с визуализацией задачи из GKLS генератора с номером 39
    """
    problem = GKLS(2, 39)

    params = SolverParameters(r=3.5, eps=0.01, itersLimit=300, refineSolution=True)
    solver = Solver(problem, parameters=params)
    
    cfol = ConsoleFullOutputListener(mode=2)
    solver.AddListener(cfol)
    apl = AnimationNDPaintListener("GKLSanim.png", "output", varsIndxs=[0,1], toPaintObjFunc=True)
    solver.AddListener(apl)
    spl = StaticNDPaintListener("GKLS.png", "output", varsIndxs=[0,1], mode="lines layers", calc="objective function")
    solver.AddListener(spl)
    spl3D = StaticNDPaintListener("GKLS3D.png", "output", varsIndxs=[0,1], mode="surface", calc="approximation")
    solver.AddListener(spl3D)

    sol = solver.Solve()


def SolveGKLSSet():
    """
    Запуск решения серии из 100 задач GKLS генератора
    """
    dim = 2
    epsVal = 0.01
    rVal = 5.1

    for i in range(100): 
        problem = GKLS(dim, i+1)
        params = SolverParameters(r=rVal, eps=epsVal, itersLimit=100000, refineSolution=False)
        solver = Solver(problem, parameters=params)
        sol = solver.Solve()

        fabsx = 0
        fm = 0
        isSolve = 0
        res = True
        for j in range(dim): 
            fabsx = np.abs(problem.knownOptimum[0].point.floatVariables[j] - sol.bestTrials[0].point.floatVariables[j])
            fm = epsVal * (problem.upperBoundOfFloatVariables[j] - problem.lowerBoundOfFloatVariables[j]);
            if (fabsx > fm):
                res = res and False

    
        if res == True:
            isSolve = 1
        print(i+1, sol.numberOfGlobalTrials, isSolve)


if __name__ == "__main__":
    SolveSingleGKLS()
    SolveGKLSSet()