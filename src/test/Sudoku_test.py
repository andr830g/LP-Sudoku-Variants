import os
import sys
sys.path.insert(0, os.getcwd())

import unittest
import numpy as np
from src.framework.Enums import Status, Variants, variants_default
from src.prod.Sudoku import Sudoku
from src.prod.solvers.PULPSolver import PULPSolver


class TestSudokuMethods(unittest.TestCase):
    input = np.array([[4, 3, 5, 2, 6, 9, 7, 8, 1],
                      [6, 8, 2, 5, 7, 1, 4, 9, 3],
                      [1, 9, 7, 8, 3, 4, 5, 6, 2],
                      [8, 2, 6, 1, 9, 5, 3, 5, 7],
                      [3, 7, 4, 6, 8, 2, 9, 1, 5],
                      [9, 5, 1, 7, 4, 3, 6, 2, 8],
                      [5, 1, 9, 3, 2, 6, 8, 7, 4],
                      [2, 4, 8, 9, 5, 7, 1, 3, 6],
                      [7, 6, 3, 4, 1, 8, 2, 5, 9]])
    
    output = '[[4 3 5 2 6 9 7 8 1]\n[6 8 2 5 7 1 4 9 3]\n[1 9 7 8 3 4 5 6 2]\n[8 2 6 1 9 5 3 5 7]\n[3 7 4 6 8 2 9 1 5]\n[9 5 1 7 4 3 6 2 8]\n[5 1 9 3 2 6 8 7 4]\n[2 4 8 9 5 7 1 3 6]\n[7 6 3 4 1 8 2 5 9]]'
    
    def test_print_without_spaces(self):
        solver = PULPSolver()
        sudoku = Sudoku(input_matrix=self.input, input_solverStrategy=solver)
        result = str(sudoku)
        
        self.assertEqual(result, self.output)
    


class TestMatrixProperties(unittest.TestCase):
    input = np.array([[4, 3, 5, 2, 6, 9, 7, 8, 1],
                      [6, 8, 2, 5, 7, 1, 4, 9, 3],
                      [1, 9, 7, 8, 3, 4, 5, 6, 2],
                      [8, 2, 6, 1, 9, 5, 3, 5, 7],
                      [3, 7, 4, 6, 8, 2, 9, 1, 5],
                      [9, 5, 1, 7, 4, 3, 6, 2, 8],
                      [5, 1, 9, 3, 2, 6, 8, 7, 4],
                      [2, 4, 8, 9, 5, 7, 1, 3, 6],
                      [7, 6, 3, 4, 1, 8, 2, 5, 9]])
    
    def test_number_of_rows(self):
        solver = PULPSolver()
        sudoku = Sudoku(input_matrix=self.input, input_solverStrategy=solver)
        rows = sudoku.getRows()
        self.assertEqual(rows, 9)
    

    def test_number_of_cols(self):
        solver = PULPSolver()
        sudoku = Sudoku(input_matrix=self.input, input_solverStrategy=solver)
        cols = sudoku.getCols()
        self.assertEqual(cols, 9)
    

    def test_get_element_at_position(self):
        solver = PULPSolver()
        sudoku = Sudoku(input_matrix=self.input, input_solverStrategy=solver)
        element = sudoku.getElementAtPosition(3, 1)
        self.assertEqual(element, 1)

        element = sudoku.getElementAtPosition(3, 9)
        self.assertEqual(element, 2)

        element = sudoku.getElementAtPosition(1, 5)
        self.assertEqual(element, 6)

        element = sudoku.getElementAtPosition(9, 5)
        self.assertEqual(element, 1)


    def test_get_elements_at_row(self):
        output = np.array([1, 9, 7, 8, 3, 4, 5, 6, 2])

        solver = PULPSolver()
        sudoku = Sudoku(input_matrix=self.input, input_solverStrategy=solver)
        row = sudoku.getRow(3)

        self.assertTrue(np.all(row == output))
    

    def test_get_elements_at_col(self):
        output = np.array([6, 7, 3, 9, 8, 4, 2, 5, 1])

        solver = PULPSolver()
        sudoku = Sudoku(input_matrix=self.input, input_solverStrategy=solver)
        col = sudoku.getCol(5)
        self.assertTrue(np.all(col == output))
    

    def test_get_nothing_at_illegal_row_and_col(self):
        solver = PULPSolver()
        sudoku = Sudoku(input_matrix=self.input, input_solverStrategy=solver)
        result = sudoku.getElementAtPosition(0, 0)
        self.assertEqual(result, None)



class TestSolveOrdinary(unittest.TestCase): 
    def test_default_variants(self):
        input = np.array([[0, 3, 5, 6, 7, 0, 0, 0, 0],
                          [4, 0, 0, 8, 2, 9, 5, 0, 0],
                          [0, 8, 0, 0, 0, 3, 0, 6, 0],
                          [0, 2, 0, 0, 0, 5, 8, 0, 7],
                          [8, 0, 0, 2, 0, 6, 0, 0, 5],
                          [3, 0, 1, 7, 0, 0, 0, 2, 0],
                          [0, 4, 0, 9, 0, 0, 0, 7, 0],
                          [0, 0, 2, 4, 8, 7, 0, 0, 6],
                          [0, 0, 0, 0, 5, 2, 4, 9, 0]])
        
        solver = PULPSolver()
        sudoku = Sudoku(input_matrix=input, input_solverStrategy=solver)
        result = sudoku.getVariants()

        self.assertEqual(result, variants_default)
    

    def test_solve_ordinary_without_squares(self):
        variants = {Variants.SQUARES:False}
        input = np.array([[0, 0, 3, 0, 5, 6, 0, 8, 9],
                          [0, 3, 4, 5, 6, 0, 0, 0, 0],
                          [3, 0, 5, 6, 7, 0, 9, 1, 2],
                          [4, 0, 0, 0, 0, 9, 1, 0, 3],
                          [0, 6, 7, 0, 9, 0, 2, 0, 4],
                          [6, 7, 8, 9, 1, 2, 3, 4, 5],
                          [7, 8, 9, 0, 2, 0, 4, 0, 6],
                          [8, 0, 1, 2, 3, 4, 5, 6, 0],
                          [9, 1, 2, 0, 4, 5, 6, 7, 8]])
        
        output = np.array([[1, 2, 3, 4, 5, 6, 7, 8, 9],
                           [2, 3, 4, 5, 6, 7, 8, 9, 1],
                           [3, 4, 5, 6, 7, 8, 9, 1, 2],
                           [4, 5, 6, 7, 8, 9, 1, 2, 3],
                           [5, 6, 7, 8, 9, 1, 2, 3, 4],
                           [6, 7, 8, 9, 1, 2, 3, 4, 5],
                           [7, 8, 9, 1, 2, 3, 4, 5, 6],
                           [8, 9, 1, 2, 3, 4, 5, 6, 7],
                           [9, 1, 2, 3, 4, 5, 6, 7, 8]])
        
        solver = PULPSolver()
        sudoku = Sudoku(input_matrix=input, input_solverStrategy=solver, input_variants=variants)
        result, status = sudoku.solve()
        
        self.assertEqual(status, Status.SOLVED)
        self.assertTrue(np.all(result == output))
    

    def test_solve_ordinary_sudoku_1(self):
        input = np.array([[0, 3, 5, 6, 7, 0, 0, 0, 0],
                          [4, 0, 0, 8, 2, 9, 5, 0, 0],
                          [0, 8, 0, 0, 0, 3, 0, 6, 0],
                          [0, 2, 0, 0, 0, 5, 8, 0, 7],
                          [8, 0, 0, 2, 0, 6, 0, 0, 5],
                          [3, 0, 1, 7, 0, 0, 0, 2, 0],
                          [0, 4, 0, 9, 0, 0, 0, 7, 0],
                          [0, 0, 2, 4, 8, 7, 0, 0, 6],
                          [0, 0, 0, 0, 5, 2, 4, 9, 0]])
    
        output = np.array([[1, 3, 5, 6, 7, 4, 9, 8, 2],
                           [4, 7, 6, 8, 2, 9, 5, 1, 3],
                           [2, 8, 9, 5, 1, 3, 7, 6, 4],
                           [6, 2, 4, 1, 9, 5, 8, 3, 7],
                           [8, 9, 7, 2, 3, 6, 1, 4, 5],
                           [3, 5, 1, 7, 4, 8, 6, 2, 9],
                           [5, 4, 3, 9, 6, 1, 2, 7, 8],
                           [9, 1, 2, 4, 8, 7, 3, 5, 6],
                           [7, 6, 8, 3, 5, 2, 4, 9, 1]])
        
        solver = PULPSolver()
        sudoku = Sudoku(input_matrix=input, input_solverStrategy=solver)
        result, status = sudoku.solve()

        self.assertEqual(status, Status.SOLVED)
        self.assertTrue(np.all(result == output))
    

    def test_solve_ordinary_sudoku_2(self):
        input = np.array([[1, 0, 0, 2, 8, 0, 5, 0, 0],
                          [0, 0, 0, 0, 0, 4, 0, 0, 0],
                          [0, 2, 0, 0, 3, 0, 0, 0, 0],
                          [0, 0, 7, 9, 0, 0, 0, 8, 0],
                          [0, 8, 0, 0, 4, 7, 9, 0, 1],
                          [0, 3, 0, 0, 0, 0, 2, 0, 6],
                          [0, 0, 0, 3, 0, 2, 6, 0, 0],
                          [0, 6, 4, 0, 0, 1, 0, 9, 0],
                          [7, 0, 0, 0, 0, 6, 8, 0, 0]])
    
        output = np.array([[1, 4, 3, 2, 8, 9, 5, 6, 7],
                           [5, 7, 8, 1, 6, 4, 3, 2, 9],
                           [9, 2, 6, 7, 3, 5, 1, 4, 8],
                           [6, 1, 7, 9, 2, 3, 4, 8, 5],
                           [2, 8, 5, 6, 4, 7, 9, 3, 1],
                           [4, 3, 9, 5, 1, 8, 2, 7, 6],
                           [8, 9, 1, 3, 7, 2, 6, 5, 4],
                           [3, 6, 4, 8, 5, 1, 7, 9, 2],
                           [7, 5, 2, 4, 9, 6, 8, 1, 3]])
        
        solver = PULPSolver()
        sudoku = Sudoku(input_matrix=input, input_solverStrategy=solver)
        result, status = sudoku.solve()

        self.assertEqual(status, Status.SOLVED)
        self.assertTrue(np.all(result == output))
    
    
    def test_no_solution_ordinary_sudoku(self):
        input = np.array([[1, 2, 0, 2, 8, 0, 5, 0, 0],
                          [0, 0, 0, 0, 0, 4, 0, 0, 0],
                          [0, 2, 0, 0, 3, 0, 0, 0, 0],
                          [0, 0, 7, 9, 0, 0, 0, 8, 0],
                          [0, 8, 0, 0, 4, 7, 9, 0, 1],
                          [0, 3, 0, 0, 0, 0, 2, 0, 6],
                          [0, 0, 0, 3, 0, 2, 6, 0, 0],
                          [0, 6, 4, 0, 0, 1, 0, 9, 0],
                          [7, 0, 0, 0, 0, 6, 8, 0, 0]])
        
        solver = PULPSolver()
        sudoku = Sudoku(input_matrix=input, input_solverStrategy=solver)
        result, status = sudoku.solve()
        self.assertEqual(status, Status.NO_SOLUTION)



class TestSolveDiagonal(unittest.TestCase):
    def test_add_diagonal_rule(self):
        variants = {Variants.DIAGONAL:True}
        input = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 7, 0, 9, 0, 0, 0],
                          [0, 0, 6, 0, 3, 0, 9, 0, 0],
                          [0, 6, 0, 2, 7, 5, 0, 1, 0],
                          [0, 0, 5, 9, 0, 6, 3, 0, 0],
                          [0, 1, 0, 3, 4, 8, 0, 9, 0],
                          [0, 0, 7, 0, 8, 0, 5, 0, 0],
                          [0, 0, 0, 4, 0, 7, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0]])
        
        solver = PULPSolver()
        sudoku = Sudoku(input_matrix=input, input_solverStrategy=solver, input_variants=variants)

        self.assertEqual(sudoku.getVariants()[Variants.DIAGONAL], True)


    def test_solve_diagonal_rule(self):
        variants = {Variants.DIAGONAL: True}
        input = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 7, 0, 9, 0, 0, 0],
                          [0, 0, 6, 0, 3, 0, 9, 0, 0],
                          [0, 6, 0, 2, 7, 5, 0, 1, 0],
                          [0, 0, 5, 9, 0, 6, 3, 0, 0],
                          [0, 1, 0, 3, 4, 8, 0, 9, 0],
                          [0, 0, 7, 0, 8, 0, 5, 0, 0],
                          [0, 0, 0, 4, 0, 7, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0]])
        
        output = np.array([[9, 5, 3, 6, 2, 1, 7, 8, 4],
                           [1, 4, 8, 7, 5, 9, 2, 6, 3],
                           [2, 7, 6, 8, 3, 4, 9, 5, 1],
                           [3, 6, 9, 2, 7, 5, 4, 1, 8],
                           [4, 8, 5, 9, 1, 6, 3, 7, 2],
                           [7, 1, 2, 3, 4, 8, 6, 9, 5],
                           [6, 3, 7, 1, 8, 2, 5, 4, 9],
                           [5, 2, 1, 4, 9, 7, 8, 3, 6],
                           [8, 9, 4, 5, 6, 3, 1, 2, 7]])
        
        solver = PULPSolver()
        sudoku = Sudoku(input_matrix=input, input_variants=variants, input_solverStrategy=solver)
        result, status = sudoku.solve()

        self.assertEqual(status, Status.SOLVED)
        self.assertTrue(np.all(result == output))



class TestSolveNonConsecutiveNeighbor(unittest.TestCase):
    def test_add_non_consecutive_neighbor_rule(self):
        variants = {Variants.NON_CONSECUTIVE_NEIGHBOR:True}
        input = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 7, 0, 9, 0, 0, 0],
                          [0, 0, 6, 0, 3, 0, 9, 0, 0],
                          [0, 6, 0, 2, 7, 5, 0, 1, 0],
                          [0, 0, 5, 9, 0, 6, 3, 0, 0],
                          [0, 1, 0, 3, 4, 8, 0, 9, 0],
                          [0, 0, 7, 0, 8, 0, 5, 0, 0],
                          [0, 0, 0, 4, 0, 7, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0]])
        
        solver = PULPSolver()
        sudoku = Sudoku(input_matrix=input, input_solverStrategy=solver, input_variants=variants)

        self.assertEqual(sudoku.getVariants()[Variants.NON_CONSECUTIVE_NEIGHBOR], True)
    

    def test_solve_non_consecutive_neighbor_rule(self):
        variants = {Variants.NON_CONSECUTIVE_NEIGHBOR:True}

        input = np.array([[5, 0, 9, 6, 0, 0, 0, 0, 4],
                          [0, 0, 6, 0, 1, 0, 5, 0, 0],
                          [0, 1, 0, 0, 0, 0, 0, 8, 0],
                          [0, 0, 1, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 7, 0],
                          [0, 0, 0, 0, 0, 0, 9, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 9, 0],
                          [0, 0, 7, 0, 9, 0, 8, 0, 0],
                          [3, 0, 0, 0, 0, 0, 0, 0, 0]])
        
        output = np.array([[5, 3, 9, 6, 8, 2, 7, 1, 4],
                           [2, 8, 6, 4, 1, 7, 5, 3, 9],
                           [7, 1, 4, 9, 3, 5, 2, 8, 6],
                           [4, 7, 1, 3, 5, 9, 6, 2, 8],
                           [9, 5, 3, 8, 2, 6, 4, 7, 1],
                           [6, 2, 8, 1, 7, 4, 9, 5, 3],
                           [8, 6, 2, 7, 4, 1, 3, 9, 5],
                           [1, 4, 7, 5, 9, 3, 8, 6, 2],
                           [3, 9, 5, 2, 6, 8, 1, 4, 7]])
        
        solver = PULPSolver()
        sudoku = Sudoku(input_matrix=input, input_solverStrategy=solver, input_variants=variants)
        result, status = sudoku.solve()

        self.assertEqual(status, Status.SOLVED)
        self.assertTrue(np.all(result == output))



if __name__ == '__main__':
    unittest.main()