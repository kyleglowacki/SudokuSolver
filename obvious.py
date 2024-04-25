import sudoku_utils as su

def sudoku_rule_error(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col].get_digit() is None:
                if len(grid[row][col].get_possible_digits()) == 0:
                    print(f"ERROR - {row},{col} has no options left.")
                    return False, grid
    return False, grid

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
def diff2(c1, c2):
    if (c1.get_row() == c2.get_row()) and (c1.get_column() == c2.get_column()):
        return False
    return True
def diff3(c1, c2, c3):
    if (c1.get_row() == c2.get_row()) and (c1.get_column() == c2.get_column()):
        return False
    if (c1.get_row() == c3.get_row()) and (c1.get_column() == c3.get_column()):
        return False
    if (c3.get_row() == c2.get_row()) and (c3.get_column() == c2.get_column()):
        return False
    return True

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
                    if diff2(c1, c2):
                        if same_possible(c1, c2):
                            print(f"Found {c1.get_row()},{c1.get_column()} and {c2.get_row()},{c2.get_column()} are the same pair {c1.get_possible_digits()}")
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
                        print(f"Remove {d1} from {row},{col}")
                        grid[row][col].remove_possible_digit(d1)
                        updates = True
                    if d2 in grid[row][col].get_possible_digits():
                        print(f"Remove {d2} from {row},{col}")
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

def rule_find_pairs_and_triples(grid):
    changes_made = False

    # Find pairs and triples with same possible digits in rows
    for row in range(9):
        cells_with_two_or_three_digits = [cell for cell in grid[row] if 2 <= len(cell.get_possible_digits()) <= 3]
        digit_combinations = {}

        for cell in cells_with_two_or_three_digits:
            possible_digits = cell.get_possible_digits()
            if len(possible_digits) == 2 or len(possible_digits) == 3:
                key = tuple(sorted(possible_digits))
                if key in digit_combinations:
                    digit_combinations[key].append(cell)
                else:
                    digit_combinations[key] = [cell]

        for key, cells in digit_combinations.items():
            if len(cells) == len(key):  # Pair or triple found
                cells_with_change = [cell for cell in grid[row] if cell not in cells and not cell.get_digit()]
                for cell in cells_with_change:
                    changes = set(cell.get_possible_digits()) - set(key)
                    if changes:
                        for digit in changes:
                            cell.remove_possible_digit(digit)
                        changes_made = True

    # Repeat the same process for columns and boxes

    return changes_made, grid

# Look at each of the nine 3x3 boxes. Then look at each digit, 1-9.  If, 
# within that box, all of the possible locations occur in the same row or 
# same column, then that digit must be within that row or column in that box 
# and therefore can be removed from the possible digits list of the rest of 
# that row/column outside of that 3x3 box as applicable
#
def sudoku_rule_box_line_reduction(grid):
    changes_made = False

    # Check each 3x3 box
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            for digit in range(1, 10):
                possible_locations = []
                for row in range(box_row, box_row + 3):
                    for col in range(box_col, box_col + 3):
                        cell = grid[row][col]
                        if digit in cell.get_possible_digits():
                            possible_locations.append((row, col))

                # Check if all possible locations occur in the same row
                same_row = all(row == possible_locations[0][0] for row, _ in possible_locations)
                if same_row:
                    row = possible_locations[0][0]
                    for col in range(9):
                        if col < box_col or col >= box_col + 3:
                            cell = grid[row][col]
                            if digit in cell.get_possible_digits():
                                cell.remove_possible_digit(digit)
                                changes_made = True

                # Check if all possible locations occur in the same column
                same_col = all(col == possible_locations[0][1] for _, col in possible_locations)
                if same_col:
                    col = possible_locations[0][1]
                    for row in range(9):
                        if row < box_row or row >= box_row + 3:
                            cell = grid[row][col]
                            if digit in cell.get_possible_digits():
                                cell.remove_possible_digit(digit)
                                changes_made = True

    return changes_made, grid
