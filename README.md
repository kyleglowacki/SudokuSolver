# SudokuSolver
Python program to solve sudoku puzzles.

Provide the puzzle on the command line as a json string putting null in for blanks.
eg. python ss.py -p [[null, null, 9, null, 1, 6, null, 8, null], [null, null, null, null, null, null, 7, null, null], [null, null, null, null, null, null, null, null, null], [6, null, 7, 3, null, 9, 8, null, null], [null, 2, null, null, null, 8, null, 4, 7], [null, 1, 3, null, 4, null, 9, null, null], [1, null, null, null, 5, null, null, null, null], [null, null, null, 9, null, null, 5, 2, null], [null, null, null, 4, null, null, 6, null, 3]]

The solver should pick up rules in python files in the same directory and invoke the rules provided they are named sudoku_rule*.  The function should return a boolean followed by an updated grid of cells. The boolean indicates an update was made (or not).
