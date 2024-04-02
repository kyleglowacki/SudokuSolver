class Cell:
    def __init__(self, digit=None):
        self.digit = digit
        self.possible_digits = set(range(1, 10)) if digit is None else set()

    def set_digit(self, digit):
        self.digit = digit
        self.possible_digits = set()

    def remove_possible_digit(self, digit):
        self.possible_digits.discard(digit)

    def get_digit(self):
        return self.digit

    def get_possible_digits(self):
        return self.possible_digits
      
    # These are to allow Cells to be used in sets and such (helpful for solving)
    def __hash__(self):
        return hash(self.digit)
    def __eq__(self, other):
        return isinstance(other, Cell) and self.digit == other.digit

def get_column(grid, column):
    return [row[column] for row in grid]

def get_row(grid, row):
    return grid[row]

def set_digit_on_grid(grid, i, j, digit):
    grid[i][j].set_digit(digit)
    if digit is not None:
        for k in range(9):
            grid[i][k].remove_possible_digit(digit)  # Remove digit from row
            grid[k][j].remove_possible_digit(digit)  # Remove digit from column

            box_row = (i // 3) * 3
            box_col = (j // 3) * 3
            for x in range(box_row, box_row + 3):
                for y in range(box_col, box_col + 3):
                    grid[x][y].remove_possible_digit(digit)  # Remove digit from box
    return grid

