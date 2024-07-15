from abc import ABC, abstractmethod
import numpy as np

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
    def __str__(self) -> str:
        pass

    @abstractmethod
    def solve(self) -> np.array:
        pass