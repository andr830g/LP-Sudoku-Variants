import os
import sys
sys.path.insert(0, os.getcwd())

import pulp as PLP
from copy import deepcopy


class Sudoku():
    def __init__(self, matrix):
        self._matrix = matrix
        self._matrix_extension = self.extendMatrix(self._matrix)

        # parameters
        self._square_row_length = 3
        self._square_col_length = 3

    
    def extendMatrix(self, matrix):
        matrix_extension = [[]] + matrix
        for j in range(0, len(matrix_extension)):
            matrix_extension[j] = [''] + matrix_extension[j]

        return matrix_extension
    

    def getMatrix(self):
        return self._matrix
    

    def getMatrixExtension(self):
        return self._matrix_extension
    

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

        if (col < 0 or col >= self.getCols()) and (row < 0 or row >= self.getRows()):
            element = None
        elif col < 0 or col >= self.getCols():
            element = matrix[row]
        elif row < 0 or row >= self.getRows():
            element = [self.getElementAtPosition(iter_row, col+1) for iter_row in range(1, self.getRows()+1)]
        else:
            element = matrix[row][col]
        return element
    

    def __str__(self):
        matrix_str = ''
    
        # row index list
        rows = list(range(0, len(self._matrix)))
    
        for row in rows:
            matrix_row = str(self._matrix[row])

            if row == rows[-1]:
                matrix_str += matrix_row
            else:
                matrix_str += f'{matrix_row}\n'
    
        # add correct matrix notation
        matrix_str = '[' + matrix_str + ']'
    
        return matrix_str
    

    def solve(self):
        N = len(self._matrix_extension)-1
        ROW = range(1, N+1)
        COL = range(1, N+1)
        VAL = range(1, N+1)

        def objectiveFunction(Model):
            # Object function doesn't matter
            Model += PLP.lpSum([x[i][j][v] for i in ROW for j in COL for v in VAL]), "Obj"
            return Model

        def valueConstraints(Model):
            for i in ROW:
                for j in COL:
                    value = self._matrix_extension[i][j]
                    if 1 <= value and value <= N:
                        Model += x[i][j][value] == 1
            return Model
        
        def ordinaryConstraints(Model):
            for i in ROW:
                for j in COL:
                    Model += PLP.lpSum([x[i][j][v] for v in VAL]) == 1

            for v in VAL:
                for i in ROW:
                    Model += PLP.lpSum([x[i][j][v] for j in COL]) == 1
    
                for j in COL:
                    Model += PLP.lpSum([x[i][j][v] for i in ROW]) == 1

            for v in VAL:
                for offset_i in range(1, N+1, self._square_row_length):
                    for offset_j in range(1, N+1, self._square_col_length):
                        Model += PLP.lpSum([x[offset_i + i][offset_j + j][v] for i in range(0, self._square_row_length) for j in range(0, self._square_col_length)]) == 1
            return Model
        
        def formatSolutionMatrix(Model, input):
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


        # Variable defintion
        var_symbol = 'x'
        x = PLP.LpVariable.dicts(var_symbol, (ROW, COL, VAL), lowBound=0, upBound=1, cat=PLP.LpBinary)

        # Model defintion
        Model = PLP.LpProblem("Sudoku", PLP.LpMaximize)

        Model = objectiveFunction(Model)

        Model = valueConstraints(Model)
        Model = ordinaryConstraints(Model)

        Model.solve()

        matrix_solved = formatSolutionMatrix(Model, input=self._matrix)

        objective_value = PLP.value(Model.objective)
        solution_status = PLP.LpStatus[Model.status]
        return matrix_solved, objective_value, solution_status