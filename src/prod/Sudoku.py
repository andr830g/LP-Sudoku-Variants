import os
import sys
sys.path.insert(0, os.getcwd())

from src.framework.AbstractSudoku import AbstractSudoku
from src.framework.AbstractSolver import AbstractSolver
from src.framework.Enums import Status, Variants, variants_default
import numpy as np
from copy import deepcopy


class Sudoku(AbstractSudoku):
    def __init__(self, input_matrix: np.array, input_solverStrategy: AbstractSolver, input_variants: dict = None) -> None:
        self._matrix = input_matrix
        self._solverStrategy = input_solverStrategy

        self._variants = deepcopy(variants_default)
        if input_variants is not None:
            for variant, value in input_variants.items():
                self._variants[variant] = value

        # parameters
        self._square_row_length = 3
        self._square_col_length = 3
    

    def getMatrix(self) -> np.array:
        return self._matrix
    

    def getRows(self) -> int:
        matrix = self.getMatrix()
        rows = matrix.shape[0]
        return rows


    def getCols(self) -> int:
        matrix = self.getMatrix()
        cols = matrix.shape[1]
        return cols
    

    def getRow(self, row: int) -> np.array:
        matrix = self.getMatrix()
        row = matrix[row-1, :]
        return row
    

    def getCol(self, col: int) -> np.array:
        matrix = self.getMatrix()
        col = matrix[:, col-1]
        return col
    
    
    def getElementAtPosition(self, row: int, col: int) -> int:
        matrix = self.getMatrix()

        if col >= 1 and col <= self.getCols() and row >= 1 and row <= self.getRows():
            element = matrix[row-1, col-1]
        else:
            element = None
        return element
    

    def __str__(self) -> str:
        matrix_str = ''
    
        # row index list
        row_indexs = list(range(1, self.getRows()+1))

        for row_index in row_indexs:
            row = str(self.getRow(row_index))

            if row_index == row_indexs[-1]:
                matrix_str += row
            else:
                matrix_str += f'{row}\n'

        # correct matrix notation
        matrix_str = '[' + matrix_str + ']'
    
        return matrix_str
    

    def getVariants(self) -> dict[Variants]:
        return self._variants
    

    def solve(self) -> tuple[np.array, Status]:
        matrix_solved, solution_status = self._solverStrategy.solve(sudoku=self)
        return matrix_solved, solution_status