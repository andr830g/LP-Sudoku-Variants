import os
import sys
sys.path.insert(0, os.getcwd())

from abc import ABC, abstractmethod
import numpy as np

from src.framework.AbstractSolver import AbstractSolver
from src.framework.AbstractSudoku import AbstractSudoku

class BaseSolver(AbstractSolver):
    def __init__(self) -> None:
        self._use_diagonal_rule = False
        self._use_nonConsecutiveNeighbor_rule = False


    def addDiagonalRule(self) -> None:
        self._use_diagonal_rule = True

    def useDiagonalRule(self) -> bool:
        return self._use_diagonal_rule


    def addNonConsecutiveNeighborRule(self) -> None:
        self._use_nonConsecutiveNeighbor_rule = True

    def useNonConsecutiveNeighborRule(self) -> bool:
        return self._use_nonConsecutiveNeighbor_rule


    def addChessKingRule(self) -> None:
        raise NotImplementedError

    def useChessKingRule(self) -> bool:
        raise NotImplementedError


    def addChessKnightRule(self) -> None:
        raise NotImplementedError

    def useChessKnightRule(self) -> bool:
        raise NotImplementedError


    def addThermometerRule(self, thermometer_set: list) -> None:
        raise NotImplementedError

    def useThermometerRule(self, thermometer_set: list) -> bool:
        raise NotImplementedError


    def addPalindromeRule(self, palindrome_set: list) -> None:
        raise NotImplementedError

    def usePalindromeRule(self, palindrome_set: list) -> bool:
        raise NotImplementedError


    def addKropkiRule(self, kropki_set: list) -> None:
        raise NotImplementedError

    def useKropkiRule(self, kropki_set: list) -> bool:
        raise NotImplementedError


    def addXVRule(self, xv_set: list) -> None:
        raise NotImplementedError

    def useXVRule(self, xv_set: list) -> bool:
        raise NotImplementedError


    def addKillerRule(self, killer_set: list) -> None:
        raise NotImplementedError

    def useKillerRule(self, killer_set: list) -> bool:
        raise NotImplementedError


    @abstractmethod
    def solve(self, sudoku: AbstractSudoku) -> np.array:
        pass