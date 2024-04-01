# SudokuSolver
Python program to solve sudoku puzzles.

Provide the puzzle on the command line as a json string putting null in for blanks.
eg. python ss.py '{"grid": [[5, null, null, 9, null, null, null, null, 1], ... ]}'

The solver should pick up rules in python files in the same directory and invoke the rules provided they are named sudoku_rule*.  The function should return a boolean and the updated grid of cells. The boolean indicates an update was made (or not).
