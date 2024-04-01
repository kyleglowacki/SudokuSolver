import inspect
import json
import sys

import sudoku_utils as su

# Also need to call to exclude set digits from all the various other cells that it is no longer possible for
def read_puzzle_from_json(json_string):
    data = json.loads(json_string)
    grid_data = data['grid']
    grid = [[su.Cell(grid_data[i][j]) if grid_data[i][j] is not None else su.Cell() for j in range(9)] for i in range(9)]
    return grid


def check_grid_validity(grid):
    if len(grid) != 9:
        return False
    for row in grid:
        if len(row) != 9:
            return False
        for cell in row:
            if not isinstance(cell, su.Cell):
                return False
            if cell.get_digit() is None:
                pass
            if cell.get_digit() < 1:
                print("Invalid value.. less than one")
                return False
            if cell.get_digit() > 9:
                print("Invalid value.. greater than nine")
                return False
    return True

def print_grid(grid):
    # Print the resulting grid
    for row in grid:
        for cell in row:
            print(cell.get_digit() if cell.get_digit() else " ", end=" ")
        print()  


def mark_initial_values(grid):
    for i in range(9):
        for j in range(9):
            digit = grid[i][j].get_digit()
            if digit is not None:
                grid = set_digit_on_grid(grid, i,j,digit)
    return grid

def is_valid_set(numbers):
    seen = set()
    for num in numbers:
        if num is not None:
            if num in seen:
                return False
            seen.add(num)
    return True
  
def is_sudoku_solved(grid):
    # Check each row
    for row in grid:
        if not is_valid_set(row):
            return False

    # Check each column
    for col in range(9):
        column = [grid[row][col] for row in range(9)]
        if not is_valid_set(column):
            return False

    # Check each box
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            box = [grid[row][col] for row in range(box_row, box_row + 3) for col in range(box_col, box_col + 3)]
            if not is_valid_set(box):
                return False
    return True

def register_rules():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    rule_files = [file for file in os.listdir(current_dir) if file.endswith('.py') and file != __file__]

    rule_functions = []
    for file in rule_files:
        module_name = os.path.splitext(file)[0]
        module_path = os.path.join(current_dir, file)

        try:
            module = __import__(module_name)
            members = inspect.getmembers(module)
            for name, member in members:
                if name.startswith('sudoku_rule_') and inspect.isfunction(member):
                    rule_functions.append(member)
        except Exception as e:
            print(f"Failed to import module {module_name}: {e}")

    return rule_functions


ex = """
{
  "grid": [
    [5, null, null, 9, null, null, null, null, 1],
    [null, null, null, null, 5, 1, null, null, null],
    [7, null, null, null, null, null, null, 4, 6],
    [null, null, null, 8, null, null, 5, null, null],
    [null, 1, null, null, null, null, null, 2, null],
    [null, null, 3, null, null, 5, null, null, null],
    [6, 7, null, null, null, null, null, null, 2],
    [null, null, null, 3, 4, null, null, null, null],
    [2, null, null, null, null, 6, null, null, 7]
  ]
}
"""

#row_7 = get_row(grid, 7)
#column_3 = get_column(grid, 3)
def main():
    # Check if a JSON string is provided as a command-line argument
    if len(sys.argv) < 2:
        print("Please provide a JSON string as a command-line argument.")
        return

    json_string = sys.argv[1]

    # Call the read_puzzle_from_json function to get the grid
    grid = read_puzzle_from_json(json_string)

    # If the grid isn't valid, error out
    if not check_grid_validity(grid):
        print("Resulting grid wasn't 9x9 containing valid cells")
        exit()

    # Mark off initial values
    grid = mark_initial_values(grid)
  
    # Print the resulting grid
    print_grid(grid)

    # Initialize the list of rule functions from files in the same directory
    rule_functions = register_rules()
    # rule_functions = [rule_1, rule_2]

    # Call each rule function and store the changes and updated grid
    any_updates = False
    for rule_func in rule_functions:
        changes_made, updated_grid = rule_func(grid)
        any_updates = any_updates or changes_made

    # figure out if done
    if is_sudoku_solved(grid):
        print("Final solution reached.")
        print_grid(grid)
        exit()
  
    if not any_updates:
        print("No updates were made this cycle... this is as far as the solver can go")
        print_grid(grid)
        exit()

if __name__ == "__main__":
    main()
