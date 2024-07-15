import os
import sys
sys.path.insert(0, os.getcwd())

from abc import ABC, abstractmethod
import numpy as np

from src.framework.AbstractSudoku import AbstractSudoku
from src.framework.Enums import Status


class AbstractSolver(ABC):
    @abstractmethod
    def solve(self, sudoku: AbstractSudoku) -> tuple[np.array, Status]:
        pass