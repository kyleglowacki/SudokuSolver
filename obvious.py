import sudoku_utils

def sudoku_rule_last_in_row(grid):
    updates = False
    # loop over rows.
    for row in range(9):
        nums = set()
        for col in range(9):
            nums.add(grid[row][col])
        # check and see if 8/9 of the row are decide
        if len(nums) == 8:
            for val in range(1,10):
                # if so.. mark blank with missing number.
                if val not in nums:
                    for col in range(9):
                        if grid[row][col] == None:
                            grid = set_digit_on_grid(grid, row, col, val)
                            updates = True
    return updates, grid

def sudoku_rule_last_in_col(grid):
    updates = False
    # loop over rows.
    for col in range(9):
        nums = set()
        for row in range(9):
            nums.add(grid[row][col])
        # check and see if 8/9 of the row are decide
        if len(nums) == 8:
            for val in range(1,10):
                # if so.. mark blank with missing number.
                if val not in nums:
                    for row in range(9):
                        if grid[row][col] == None:
                            grid = set_digit_on_grid(grid, row, col, val)
                            updates = True
    return updates, grid
