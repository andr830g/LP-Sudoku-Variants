import os
import sys
sys.path.insert(0, os.getcwd())

import unittest
from src.prod.Sudoku import Sudoku


class TestPrintFunction(unittest.TestCase):
    matrix_str = '[[4, 3, 5, 2, 6, 9, 7, 8, 1]\n[6, 8, 2, 5, 7, 1, 4, 9, 3]\n[1, 9, 7, 8, 3, 4, 5, 6, 2]\n[8, 2, 6, 1, 9, 5, 3, 5, 7]\n[3, 7, 4, 6, 8, 2, 9, 1, 5]\n[9, 5, 1, 7, 4, 3, 6, 2, 8]\n[5, 1, 9, 3, 2, 6, 8, 7, 4]\n[2, 4, 8, 9, 5, 7, 1, 3, 6]\n[7, 6, 3, 4, 1, 8, 2, 5, 9]]'
    
    def test_print_without_spaces(self):
        sudoku = [[4, 3, 5, 2, 6, 9, 7, 8, 1],
                  [6, 8, 2, 5, 7, 1, 4, 9, 3],
                  [1, 9, 7, 8, 3, 4, 5, 6, 2],
                  [8, 2, 6, 1, 9, 5, 3, 5, 7],
                  [3, 7, 4, 6, 8, 2, 9, 1, 5],
                  [9, 5, 1, 7, 4, 3, 6, 2, 8],
                  [5, 1, 9, 3, 2, 6, 8, 7, 4],
                  [2, 4, 8, 9, 5, 7, 1, 3, 6],
                  [7, 6, 3, 4, 1, 8, 2, 5, 9]]
        
        sudoku = Sudoku(sudoku)
        result = str(sudoku)
        self.assertEqual(result, self.matrix_str)



if __name__ == '__main__':
    unittest.main()