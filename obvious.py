import sudoku_utils as su

# Because possible digits is maintained, this rule tends to catch nearly all
# digits while most other rules will only update the list of possible digits
def sudoku_rule_only_choice(grid):
    updates = False
    # loop over rows.
    for row in range(9):
        for col in range(9):
            if len(grid[row][col].get_possible_digits()) == 1:
                # if so.. mark blank with missing number.
                digit = list(grid[row][col].get_possible_digits())[0]
                grid = su.set_digit_on_grid(grid, row, col, digit)
                updates = True
    return updates, grid
# Covers ...
# only one blank in row can be a particular digit
# only one blank in col can be a particular digit
# only one blank in box can be a particular digit

# Return true if c1 and c2 are different cells.
def diff(c1, c2):
    return not ((c1.get_row() == c2.get_row()) and (c1.get_column() == c2.get_column))

def same_possible(c1, c2):
    pds2 = c2.get_possible_digits()
    for pd1 in c1.get_possible_digits():
        if pd1 not in pds2:
            return False
    return True
            

# helper func that finds the first pair and returns it
def process_cells(cells):
    # Find a first cell, then find its match
    for c1 in cells:
        if len(c1.get_possible_digits()) == 2:
            # Found a start.... look for a match
            for c2 in cells:
                if len(c2.get_possible_digits()) == 2:
                    if diff(c1, c2):
                        if same_possible(c1, c2):
                            digits = list(c2.get_possible_digits())
                            return True, digits[0], digits[1]
            
    return False, 0, 0


# If we have multiple blanks in a row and 2 blanks have the same 2 possible digits, then
# remove those two digits from all other blanks in the row.
def sudoku_rule_pairs_in_row(grid):
    updates = False
    # loop over rows.
    for row in range(9):
        cells = su.get_row(grid, row)

        found, d1, d2 = process_cells(cells)
        if found:
            for c in cells:
                col = c.get_column()
                if len(grid[row][col].get_possible_digits()) > 2:
                    if d1 in grid[row][col].get_possible_digits():
                        grid[row][col].remove_possible_digit(d1)
                        updates = True
                    if d2 in grid[row][col].get_possible_digits():
                        grid[row][col].remove_possible_digit(d2)
                        updates = True
    return updates, grid


# If we have multiple blanks in a col and 2 blanks have the same 2 possible digits, then
# remove those two digits from all other blanks in the col.
def sudoku_rule_pairs_in_col(grid):
    updates = False
    # loop over rows.
    for col in range(9):
        cells = su.get_column(grid, col)

        found, d1, d2 = process_cells(cells)
        if found:
            for c in cells:
                row = c.get_row()
                if len(grid[row][col].get_possible_digits()) > 2:
                    if d1 in grid[row][col].get_possible_digits():
                        grid[row][col].remove_possible_digit(d1)
                        updates = True
                    if d2 in grid[row][col].get_possible_digits():
                        grid[row][col].remove_possible_digit(d2)
                        updates = True
    return updates, grid
