import os
import sys
sys.path.insert(0, os.getcwd())

import pulp as PLP
from copy import deepcopy


class Sudoku():
    def __init__(self, matrix):
        self.matrix = matrix
        self.matrix_extension = self.extendMatrix()

        self.N = len(self.matrix_extension)-1
        self.ROW = range(1, self.N+1)
        self.COL = range(1, self.N+1)
        self.VAL = range(1, self.N+1)
        self.Model = PLP.LpProblem("Sudoku", PLP.LpMaximize)
        self.square_row_length = 3
        self.square_col_length = 3

    
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
        # variables
        var_symbol = 'x'
        x = PLP.LpVariable.dicts(var_symbol, (self.ROW, self.COL, self.VAL), lowBound=0, upBound=1, cat=PLP.LpBinary)

        # Object function doesn't matter
        self.Model += PLP.lpSum([x[i][j][v] for i in self.ROW for j in self.COL for v in self.VAL]), "Obj"

        # input
        for i in self.ROW:
            for j in self.COL:
                value = self.matrix_extension[i][j]
                if 1 <= value and value <= self.N:
                    self.Model += x[i][j][value] == 1
        
        # Ordinary Sudoku constraints
        for i in self.ROW:
            for j in self.COL:
                self.Model += PLP.lpSum([x[i][j][v] for v in self.VAL]) == 1

        for v in self.VAL:
            for i in self.ROW:
                self.Model += PLP.lpSum([x[i][j][v] for j in self.COL]) == 1
    
            for j in self.COL:
                self.Model += PLP.lpSum([x[i][j][v] for i in self.ROW]) == 1

        for v in self.VAL:
            for offset_i in range(1, self.N+1, self.square_row_length):
                for offset_j in range(1, self.N+1, self.square_col_length):
                    self.Model += PLP.lpSum([x[offset_i + i][offset_j + j][v] for i in range(0, self.square_row_length) for j in range(0, self.square_col_length)]) == 1
        
        self.Model.solve()

        matrix_solved = deepcopy(self.matrix)
        for value in self.Model.variables():
            list_var_name = value.name.split('_')
            if list_var_name[0] == var_symbol:
                i = int(list_var_name[1]) - 1
                j = int(list_var_name[2]) - 1
                v = int(list_var_name[3])
                if value.varValue == 1:
                    matrix_solved[i][j] = v
            else:
                print(value.name + '=' + str(value.varValue))

        return matrix_solved