from abc import ABC, abstractmethod

class AbstractSolver(ABC):
    @abstractmethod
    def addDiagonalRule(self):
        pass

    @abstractmethod
    def useDiagonalRule(self):
        pass
    

    @abstractmethod
    def addNonConsecutiveNeighborRule(self):
        pass

    @abstractmethod
    def useNonConsecutiveNeighborRule(self):
        pass

    
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