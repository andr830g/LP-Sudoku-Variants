from abc import ABC, abstractmethod

class AbstractSudoku(ABC):
    @abstractmethod
    def getMatrix(self):
        pass
    
    @abstractmethod
    def getRows(self):
        pass

    @abstractmethod
    def getCols(self):
        pass

    @abstractmethod
    def getElementAtPosition(self, row, col):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def solve(self):
        pass