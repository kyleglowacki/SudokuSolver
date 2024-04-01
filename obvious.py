import sudoku_utils

def sudoku_rule_only_choice(grid):
    updates = False
    # loop over rows.
    for row in range(9):
        for col in range(9):
            if len(grid[row][col].get_possible_digits()) == 1:
                # if so.. mark blank with missing number.
                grid = set_digit_on_grid(grid, row, col, grid[row][col].get_possible_digits()[0])
                updates = True
    return updates, grid

# only one blank in row can be a particular digit
# only one blank in col can be a particular digit
# only one blank in box can be a particular digit

