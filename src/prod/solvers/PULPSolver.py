import os
import sys
sys.path.insert(0, os.getcwd())

from src.framework.AbstractSudoku import AbstractSudoku
from src.framework.AbstractSolver import AbstractSolver
from src.framework.Enums import Status, Variants
import pulp as PLP
from copy import deepcopy
import numpy as np


class PULPSolver(AbstractSolver):
    def __init__(self) -> None:
        self._inf = 9999

        self._variant_map = {Variants.SQUARES:self.squareConstraints,
                             Variants.DIAGONAL:self.diagonalConstraints,
                             Variants.NON_CONSECUTIVE_NEIGHBOR:self.nonConsecutiveNeighborConstraints,
                             Variants.CHESS_KING:self.chessKingConstraints,
                             Variants.CHESS_KNIGHT:self.chessKnightConstraints,
                             Variants.THERMO:self.thermoConstraints}


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

        for key, value in sudoku.getVariants().items():
            if value == True:
                Model = self._variant_map[key](Model, sudoku, x, N, row_index, col_index, values)

        Model.solve()

        matrix_solved = self.formatSolutionMatrix(Model, sudoku.getMatrix(), var_symbol)
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

        return Model
    

    def squareConstraints(self, Model, sudoku, x, N, row_index, col_index, values) -> PLP.LpProblem:
        # each value occur once per square
        for v in values:
            for offset_i in range(1, N+1, sudoku._square_row_length):
                for offset_j in range(1, N+1, sudoku._square_col_length):
                    Model += PLP.lpSum([x[offset_i + i][offset_j + j][v] for i in range(0, sudoku._square_row_length) for j in range(0, sudoku._square_col_length)]) == 1
        return Model
    

    def diagonalConstraints(self, Model, sudoku, x, N, row_index, col_index, values) -> PLP.LpProblem:
        diagonals = [[(i, j) for i in row_index for j in col_index if i==j],
                    [(i, j) for i in row_index for j in col_index if i==N+1-j]]
        
        # each value must occur once per diagonal
        for diag in diagonals:
            for value in values:
                Model += PLP.lpSum([x[i][j][value] for (i, j) in diag]) == 1

        return Model
    

    def nonConsecutiveNeighborConstraints(self, Model, sudoku, x, N, row_index, col_index, values) -> PLP.LpProblem:
        non_consecutive_delta = PLP.LpVariable.dicts("non_consecutive_delta", (range(1, (N-1)*N*2+1), [1, 2]), lowBound=0, upBound=1, cat=PLP.LpBinary)
        non_consecutive_count = 0
        for i in range(1, N+1):
            for j in range(1, N+1):
                if j < N:
                    non_consecutive_count += 1
                    Model += PLP.lpSum([x[i][j][v]*v for v in values]) - PLP.lpSum([x[i][j+1][v]*v for v in values]) - 2 >= -self._inf*(1-non_consecutive_delta[non_consecutive_count][1])
                    Model += PLP.lpSum([x[i][j+1][v]*v for v in values]) - PLP.lpSum([x[i][j][v]*v for v in values]) - 2 >= -self._inf*(1-non_consecutive_delta[non_consecutive_count][2])
                    Model += non_consecutive_delta[non_consecutive_count][1] + non_consecutive_delta[non_consecutive_count][2] == 1
                if i < N:
                    non_consecutive_count += 1
                    Model += PLP.lpSum([x[i][j][v]*v for v in values]) - PLP.lpSum([x[i+1][j][v]*v for v in values]) - 2 >= -self._inf*(1-non_consecutive_delta[non_consecutive_count][1])
                    Model += PLP.lpSum([x[i+1][j][v]*v for v in values]) - PLP.lpSum([x[i][j][v]*v for v in values]) - 2 >= -self._inf*(1-non_consecutive_delta[non_consecutive_count][2])
                    Model += non_consecutive_delta[non_consecutive_count][1] + non_consecutive_delta[non_consecutive_count][2] == 1
        return Model
    

    def chessKingConstraints(self, Model, sudoku, x, N, row_index, col_index, values) -> PLP.LpProblem:
        for i in row_index:
            for j in col_index:
                chess_king_points = [(i+a, j+b) for a in [-1, 1] for b in [-1, 1] if i+a >= 1 and i+a <= N and j+b >= 1 and j+b <= N]
                for v in values:
                    Model += PLP.lpSum([x[a][b][v] for (a, b) in chess_king_points]) <= 4*(1-x[i][j][v])
        return Model
    

    def chessKnightConstraints(self, Model, sudoku, x, N, row_index, col_index, values) -> PLP.LpProblem:
        for i in row_index:
            for j in col_index:
                chess_knight_points = [(i+a, j+b) for (a, b) in [(1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1)] 
                                       if i+a >= 1 and i+a <= N and j+b >= 1 and j+b <= N]
                for v in values:
                    Model += PLP.lpSum([x[a][b][v] for (a, b) in chess_knight_points]) <= 8*(1-x[i][j][v])
        return Model
    

    def thermoConstraints(self, Model, sudoku, x, N, row_index, col_index, values) -> PLP.LpProblem:
        for shape in sudoku.getShape(Variants.THERMO):
            while len(shape) >= 2:
                p1 = shape[0]
                p2 = shape[1]
                Model += PLP.lpSum([x[p1[0]][p1[1]][v]*v for v in values]) <= PLP.lpSum([x[p2[0]][p2[1]][v]*v for v in values])
                Model += PLP.lpSum([x[p2[0]][p2[1]][v]*v for v in values]) - PLP.lpSum([x[p1[0]][p1[1]][v]*v for v in values]) >= 1
                shape.pop(0)
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