import os
import sys
sys.path.insert(0, os.getcwd())

from src.framework.AbstractSudoku import AbstractSudoku
from src.framework.AbstractSolver import AbstractSolver
from src.framework.Status import Status
import pulp as PLP
from copy import deepcopy
import numpy as np


class PULPSolver(AbstractSolver):
    def __init__(self) -> None:
        self._use_diagonal_rule = False
        self._use_nonConsecutiveNeighbor_rule = False


    def addDiagonalRule(self) -> Status:
        self._use_diagonal_rule = True
        return Status.OK

    def useDiagonalRule(self) -> bool:
        return self._use_diagonal_rule


    def addNonConsecutiveNeighborRule(self) -> Status:
        self._use_nonConsecutiveNeighbor_rule = True
        return Status.OK

    def useNonConsecutiveNeighborRule(self) -> bool:
        return self._use_nonConsecutiveNeighbor_rule


    def addChessKingRule(self) -> Status:
        raise NotImplementedError

    def useChessKingRule(self) -> bool:
        raise NotImplementedError


    def addChessKnightRule(self) -> Status:
        raise NotImplementedError

    def useChessKnightRule(self) -> bool:
        raise NotImplementedError


    def addThermometerRule(self, thermometer_set: list) -> Status:
        raise NotImplementedError

    def useThermometerRule(self, thermometer_set: list) -> bool:
        raise NotImplementedError


    def addPalindromeRule(self, palindrome_set: list) -> Status:
        raise NotImplementedError

    def usePalindromeRule(self, palindrome_set: list) -> bool:
        raise NotImplementedError


    def addKropkiRule(self, kropki_set: list) -> Status:
        raise NotImplementedError

    def useKropkiRule(self, kropki_set: list) -> bool:
        raise NotImplementedError


    def addXVRule(self, xv_set: list) -> Status:
        raise NotImplementedError

    def useXVRule(self, xv_set: list) -> bool:
        raise NotImplementedError


    def addKillerRule(self, killer_set: list) -> Status:
        raise NotImplementedError

    def useKillerRule(self, killer_set: list) -> bool:
        raise NotImplementedError


    def solve(self, sudoku: AbstractSudoku) -> tuple[np.array, Status]:
        N = sudoku.getRows()
        row_index = range(1, N+1)
        col_index = range(1, N+1)
        values = range(1, N+1)

        # Variable defintion
        var_symbol = 'x'
        x = PLP.LpVariable.dicts(var_symbol, (row_index, col_index, values), lowBound=0, upBound=1, cat=PLP.LpBinary)

        # Model defintion
        Model = PLP.LpProblem("Sudoku", PLP.LpMaximize)

        Model = self.objectiveFunction(Model, x, row_index, col_index, values)

        Model = self.valueConstraints(Model, sudoku, x, N, row_index, col_index, values)
        Model = self.ordinaryConstraints(Model, sudoku, x, N, row_index, col_index, values)

        if self.useDiagonalRule():
            Model = self.diagonalConstraints(Model, x, N, row_index, col_index, values)

        Model.solve()

        matrix_solved = self.formatSolutionMatrix(Model, sudoku.getMatrix(), var_symbol)
        #objective_value = PLP.value(Model.objective)
        solution_status = Status.SOLVED if PLP.LpStatus[Model.status] == Status.SOLVED.value else Status.NO_SOLUTION

        return matrix_solved, solution_status
    

    def objectiveFunction(self, Model, x, row_index, col_index, values) -> PLP.LpProblem:
        # Object function doesn't matter
        Model += PLP.lpSum([x[i][j][v] for i in row_index for j in col_index for v in values]), "Obj"
        return Model


    def valueConstraints(self, Model, sudoku, x, N, row_index, col_index, values) -> PLP.LpProblem:
        # each cell has the same value as the input if any
        for i in row_index:
            for j in col_index:
                value = sudoku.getElementAtPosition(row=i, col=j)
                if value in values:
                    Model += x[i][j][value] == 1
        return Model
        

    def ordinaryConstraints(self, Model, sudoku, x, N, row_index, col_index, values) -> PLP.LpProblem:
        # each cell has one value
        for i in row_index:
            for j in col_index:
                Model += PLP.lpSum([x[i][j][v] for v in values]) == 1

        for v in values:
            # each value occur once per row
            for i in row_index:
                Model += PLP.lpSum([x[i][j][v] for j in col_index]) == 1
    
            # each value occur once per column
            for j in col_index:
                Model += PLP.lpSum([x[i][j][v] for i in row_index]) == 1

        # each value occur once per square
        for v in values:
            for offset_i in range(1, N+1, sudoku._square_row_length):
                for offset_j in range(1, N+1, sudoku._square_col_length):
                    Model += PLP.lpSum([x[offset_i + i][offset_j + j][v] for i in range(0, sudoku._square_row_length) for j in range(0, sudoku._square_col_length)]) == 1
        return Model
    

    def diagonalConstraints(self, Model, x, N, row_index, col_index, values) -> PLP.LpProblem:
        diagonals = [[(i, j) for i in row_index for j in col_index if i==j],
                    [(i, j) for i in row_index for j in col_index if i==N+1-j]]
        
        # each value must occur once per diagonal
        for diag in diagonals:
            for value in values:
                Model += PLP.lpSum([x[i][j][value] for (i, j) in diag]) == 1

        return Model
    

    def formatSolutionMatrix(self, Model: PLP.LpProblem, input: np.array, var_symbol: str) -> np.array:
        matrix_solved = deepcopy(input)
        for value in Model.variables():
            list_var_name = value.name.split('_')
            if list_var_name[0] == var_symbol:
                i = int(list_var_name[1]) - 1
                j = int(list_var_name[2]) - 1
                v = int(list_var_name[3])
                if value.varValue == 1:
                    matrix_solved[i][j] = v
        return matrix_solved