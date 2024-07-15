import os
import sys
sys.path.insert(0, os.getcwd())

from src.framework.AbstractSolver import AbstractSolver
import pulp as PLP
from copy import deepcopy


class PULPSolver(AbstractSolver):
    def solve(self, sudoku):
        N = sudoku.getRows()
        row_index = range(1, N+1)
        col_index = range(1, N+1)
        values = range(1, N+1)

        def objectiveFunction(Model):
            # Object function doesn't matter
            Model += PLP.lpSum([x[i][j][v] for i in row_index for j in col_index for v in values]), "Obj"
            return Model

        def valueConstraints(Model):
            # each cell has the same value as the input if any
            for i in row_index:
                for j in col_index:
                    value = sudoku.getElementAtPosition(row=i, col=j)
                    if 1 <= value and value <= N:
                        Model += x[i][j][value] == 1
            return Model
        
        def ordinaryConstraints(Model):
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

        matrix_solved = formatSolutionMatrix(Model, input=sudoku.getMatrix())
        objective_value = PLP.value(Model.objective)
        solution_status = PLP.LpStatus[Model.status]
        return matrix_solved, solution_status