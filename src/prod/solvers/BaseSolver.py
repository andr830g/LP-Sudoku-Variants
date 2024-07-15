import os
import sys
sys.path.insert(0, os.getcwd())

from abc import ABC, abstractmethod

from src.framework.AbstractSolver import AbstractSolver

class BaseSolver(AbstractSolver):
    def __init__(self) -> None:
        self._use_diagonal_rule = False
        self._use_nonConsecutiveNeighbor_rule = False


    def addDiagonalRule(self):
        self._use_diagonal_rule = True

    def useDiagonalRule(self):
        return self._use_diagonal_rule


    def addNonConsecutiveNeighborRule(self):
        self._use_nonConsecutiveNeighbor_rule = True

    def useNonConsecutiveNeighborRule(self):
        return self._use_nonConsecutiveNeighbor_rule


    @abstractmethod
    def addChessKingRule(self):
        pass

    @abstractmethod
    def useChessKingRule(self):
        pass


    @abstractmethod
    def addChessKnightRule(self):
        pass

    @abstractmethod
    def useChessKnightRule(self):
        pass


    @abstractmethod
    def addThermometerRule(self, thermometer_set):
        pass

    @abstractmethod
    def useThermometerRule(self, thermometer_set):
        pass


    @abstractmethod
    def addPalindromeRule(self, palindrome_set):
        pass

    @abstractmethod
    def usePalindromeRule(self, palindrome_set):
        pass


    @abstractmethod
    def addKropkiRule(self, kropki_set):
        pass

    @abstractmethod
    def useKropkiRule(self, kropki_set):
        pass


    @abstractmethod
    def addXVRule(self, xv_set):
        pass

    @abstractmethod
    def useXVRule(self, xv_set):
        pass


    @abstractmethod
    def addKillerRule(self, killer_set):
        pass

    @abstractmethod
    def useKillerRule(self, killer_set):
        pass


    @abstractmethod
    def solve(self, sudoku):
        pass