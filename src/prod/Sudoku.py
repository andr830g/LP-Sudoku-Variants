import os
import sys
sys.path.insert(0, os.getcwd())

import pulp as PLP
from copy import deepcopy


class Sudoku():
    def __init__(self, matrix):
        self._matrix = matrix

        # parameters
        self._square_row_length = 3
        self._square_col_length = 3
    

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
        N = self.getRows()
        row_index = range(1, N+1)
        col_index = range(1, N+1)
        values = range(1, N+1)

        def objectiveFunction(Model):
            # Object function doesn't matter
            Model += PLP.lpSum([x[i][j][v] for i in row_index for j in col_index for v in values]), "Obj"
            return Model

        def valueConstraints(Model):
            for i in row_index:
                for j in col_index:
                    value = self.getElementAtPosition(row=i, col=j)
                    if 1 <= value and value <= N:
                        Model += x[i][j][value] == 1
            return Model
        
        def ordinaryConstraints(Model):
            for i in row_index:
                for j in col_index:
                    Model += PLP.lpSum([x[i][j][v] for v in values]) == 1

            for v in values:
                for i in row_index:
                    Model += PLP.lpSum([x[i][j][v] for j in col_index]) == 1
    
                for j in col_index:
                    Model += PLP.lpSum([x[i][j][v] for i in row_index]) == 1

            for v in values:
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
        x = PLP.LpVariable.dicts(var_symbol, (row_index, col_index, values), lowBound=0, upBound=1, cat=PLP.LpBinary)

        # Model defintion
        Model = PLP.LpProblem("Sudoku", PLP.LpMaximize)

        Model = objectiveFunction(Model)

        Model = valueConstraints(Model)
        Model = ordinaryConstraints(Model)

        Model.solve()

        matrix_solved = formatSolutionMatrix(Model, input=self.getMatrix())

        objective_value = PLP.value(Model.objective)
        solution_status = PLP.LpStatus[Model.status]
        return matrix_solved, objective_value, solution_status