import os
import sys
sys.path.insert(0, os.getcwd())

from src.framework.AbstractSolver import AbstractSolver

class FakeSolver(AbstractSolver):
    def solve(self, sudoku):
        return None, None