import os
import sys
sys.path.insert(0, os.getcwd())

from abc import ABC, abstractmethod
import numpy as np

from src.framework.AbstractSudoku import AbstractSudoku


class AbstractSolver(ABC):
    @abstractmethod
    def addDiagonalRule(self) -> None:
        pass

    @abstractmethod
    def useDiagonalRule(self) -> bool:
        pass
    

    @abstractmethod
    def addNonConsecutiveNeighborRule(self) -> None:
        pass

    @abstractmethod
    def useNonConsecutiveNeighborRule(self) -> bool:
        pass

    
    @abstractmethod
    def addChessKingRule(self) -> None:
        pass

    @abstractmethod
    def useChessKingRule(self) -> bool:
        pass


    @abstractmethod
    def addChessKnightRule(self) -> None:
        pass

    @abstractmethod
    def useChessKnightRule(self) -> bool:
        pass


    @abstractmethod
    def addThermometerRule(self, thermometer_set: list) -> None:
        pass

    @abstractmethod
    def useThermometerRule(self, thermometer_set: list) -> bool:
        pass


    @abstractmethod
    def addPalindromeRule(self, palindrome_set: list) -> None:
        pass

    @abstractmethod
    def usePalindromeRule(self, palindrome_set: list) -> bool:
        pass


    @abstractmethod
    def addKropkiRule(self, kropki_set: list) -> None:
        pass

    @abstractmethod
    def useKropkiRule(self, kropki_set: list) -> bool:
        pass


    @abstractmethod
    def addXVRule(self, xv_set: list) -> None:
        pass

    @abstractmethod
    def useXVRule(self, xv_set: list) -> bool:
        pass


    @abstractmethod
    def addKillerRule(self, killer_set: list) -> None:
        pass

    @abstractmethod
    def useKillerRule(self, killer_set: list) -> bool:
        pass


    @abstractmethod
    def solve(self, sudoku: AbstractSudoku) -> np.array:
        pass