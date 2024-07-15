import os
import sys
sys.path.insert(0, os.getcwd())

from abc import ABC, abstractmethod
import numpy as np
from src.framework.Enums import Variants

class AbstractSudoku(ABC):
    @abstractmethod
    def getMatrix(self) -> np.array:
        pass
    
    @abstractmethod
    def getRows(self) -> int:
        pass

    @abstractmethod
    def getCols(self) -> int:
        pass

    @abstractmethod
    def getRow(self, row: int) -> np.array:
        pass

    @abstractmethod
    def getCol(self, col: int) -> np.array:
        pass

    @abstractmethod
    def getElementAtPosition(self, row: int, col: int) -> np.array:
        pass

    @abstractmethod
    def getVariants(self) -> dict[Variants]:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def solve(self) -> np.array:
        pass