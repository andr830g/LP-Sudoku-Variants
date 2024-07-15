import os
import sys
sys.path.insert(0, os.getcwd())

from src.prod.solvers.BaseSolver import BaseSolver

class FakeSolver(BaseSolver):
    def solve(self, sudoku):
        return None, None