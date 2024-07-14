import os
import sys
sys.path.insert(0, os.getcwd())

import pulp as PLP


class Sudoku():
    def __init__(self, matrix):
        self.matrix = matrix
        self.matrix_extension = self.extendMatrix()

    
    def extendMatrix(self):
        matrix_extension = [[]] + self.matrix
        for j in range(0, len(matrix_extension)):
            matrix_extension[j] = [''] + matrix_extension[j]

        return matrix_extension
    
    def __str__(self):
        matrix_str = ''
    
        # row index list
        rows = list(range(0, len(self.matrix)))
    
        for row in rows:
            matrix_row = str(self.matrix[row])

            if row == rows[-1]:
                matrix_str += matrix_row
            else:
                matrix_str += f'{matrix_row}\n'
    
        # add correct matrix notation
        matrix_str = '[' + matrix_str + ']'
    
        return matrix_str
    

    def solve(self):
        return None