import os
import sys
sys.path.insert(0, os.getcwd())

from src.framework.AbstractSudoku import AbstractSudoku


class Sudoku(AbstractSudoku):
    def __init__(self, matrix, solverStrategy):
        self._matrix = matrix
        self._solverStrategy = solverStrategy

        # parameters
        self._square_row_length = 3
        self._square_col_length = 3
    

    def getMatrix(self):
        return self._matrix
    

    def getRows(self):
        rows = len(self.getMatrix())
        return rows
    

    def getCols(self):
        cols = len(self.getElementAtPosition(1, -1))
        return cols
    

    def getElementAtPosition(self, row, col):
        matrix = self.getMatrix()
        row = row-1
        col = col-1

        # error
        if (col < 0 or col >= self.getCols()) and (row < 0 or row >= self.getRows()):
            element = None
        # if column value is illegal then output whole row
        elif col < 0 or col >= self.getCols():
            element = matrix[row]
        # if row value is illegal then output whole column
        elif row < 0 or row >= self.getRows():
            element = [self.getElementAtPosition(iter_row, col+1) for iter_row in range(1, self.getRows()+1)]
        # if row and column values are legal then output specific element
        else:
            element = matrix[row][col]
        return element
    

    def __str__(self):
        matrix_str = ''
    
        # row index list
        rows = list(range(1, self.getRows()+1))
    
        for row in rows:
            matrix_row = str(self.getElementAtPosition(row=row, col=-1))

            if row == rows[-1]:
                matrix_str += matrix_row
            else:
                matrix_str += f'{matrix_row}\n'
    
        # add correct matrix notation
        matrix_str = '[' + matrix_str + ']'
    
        return matrix_str
    

    def solve(self):
        matrix_solved, solution_status = self._solverStrategy.solve(sudoku=self)
        return matrix_solved, solution_status