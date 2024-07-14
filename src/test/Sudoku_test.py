import os
import sys
sys.path.insert(0, os.getcwd())

import unittest
from src.prod.Sudoku import Sudoku


class TestMatrixManipulationFunctions(unittest.TestCase):
    input = [[4, 3, 5, 2, 6, 9, 7, 8, 1],
             [6, 8, 2, 5, 7, 1, 4, 9, 3],
             [1, 9, 7, 8, 3, 4, 5, 6, 2],
             [8, 2, 6, 1, 9, 5, 3, 5, 7],
             [3, 7, 4, 6, 8, 2, 9, 1, 5],
             [9, 5, 1, 7, 4, 3, 6, 2, 8],
             [5, 1, 9, 3, 2, 6, 8, 7, 4],
             [2, 4, 8, 9, 5, 7, 1, 3, 6],
             [7, 6, 3, 4, 1, 8, 2, 5, 9]]
    
    def test_print_without_spaces(self):
        sudoku = Sudoku(self.input)
        result = str(sudoku)
        self.assertEqual(result, '[[4, 3, 5, 2, 6, 9, 7, 8, 1]\n[6, 8, 2, 5, 7, 1, 4, 9, 3]\n[1, 9, 7, 8, 3, 4, 5, 6, 2]\n[8, 2, 6, 1, 9, 5, 3, 5, 7]\n[3, 7, 4, 6, 8, 2, 9, 1, 5]\n[9, 5, 1, 7, 4, 3, 6, 2, 8]\n[5, 1, 9, 3, 2, 6, 8, 7, 4]\n[2, 4, 8, 9, 5, 7, 1, 3, 6]\n[7, 6, 3, 4, 1, 8, 2, 5, 9]]')


    def test_first_row_of_extend_matrix(self):
        sudoku = Sudoku(self.input)
        result = sudoku.extendMatrix()
        self.assertEqual(result[0], [''])
    
    def test_first_element_of_rows_extend_matrix(self):
        sudoku = Sudoku(self.input)
        result = sudoku.extendMatrix()
        for row in result:
            self.assertEqual(row[0], '')
    
    def test_extend_matrix(self):
        sudoku = Sudoku(self.input)
        result = sudoku.extendMatrix()

        self.assertEqual(result, [[''], 
                                  ['', 4, 3, 5, 2, 6, 9, 7, 8, 1],
                                  ['', 6, 8, 2, 5, 7, 1, 4, 9, 3],
                                  ['', 1, 9, 7, 8, 3, 4, 5, 6, 2],
                                  ['', 8, 2, 6, 1, 9, 5, 3, 5, 7],
                                  ['', 3, 7, 4, 6, 8, 2, 9, 1, 5],
                                  ['', 9, 5, 1, 7, 4, 3, 6, 2, 8],
                                  ['', 5, 1, 9, 3, 2, 6, 8, 7, 4],
                                  ['', 2, 4, 8, 9, 5, 7, 1, 3, 6],
                                  ['', 7, 6, 3, 4, 1, 8, 2, 5, 9]])


class TestSolveOrdinary(unittest.TestCase):
    input = [[0, 3, 5, 6, 7, 0, 0, 0, 0],
             [4, 0, 0, 8, 2, 9, 5, 0, 0],
             [0, 8, 0, 0, 0, 3, 0, 6, 0],
             [0, 2, 0, 0, 0, 5, 8, 0, 7],
             [8, 0, 0, 2, 0, 6, 0, 0, 5],
             [3, 0, 1, 7, 0, 0, 0, 2, 0],
             [0, 4, 0, 9, 0, 0, 0, 7, 0],
             [0, 0, 2, 4, 8, 7, 0, 0, 6],
             [0, 0, 0, 0, 5, 2, 4, 9, 0]]
    
    output = [[1, 3, 5, 6, 7, 4, 9, 8, 2],
              [4, 7, 6, 8, 2, 9, 5, 1, 3],
              [2, 8, 9, 5, 1, 3, 7, 6, 4],
              [6, 2, 4, 1, 9, 5, 8, 3, 7],
              [8, 9, 7, 2, 3, 6, 1, 4, 5],
              [3, 5, 1, 7, 4, 8, 6, 2, 9],
              [5, 4, 3, 9, 6, 1, 2, 7, 8],
              [9, 1, 2, 4, 8, 7, 3, 5, 6],
              [7, 6, 8, 3, 5, 2, 4, 9, 1]]
    
    def test_solve_ordinary_sudoku(self):
        sudoku = Sudoku(self.input)
        result = sudoku.solve()
        self.assertEqual(result, self.output)


if __name__ == '__main__':
    unittest.main()