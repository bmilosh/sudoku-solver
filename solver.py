

PUZZLE_NOT_SOLVABLE = """
Could not solve puzzle! Please, check that enough clues are given,
all the given clues are correct, and there are no repeated entries
in grids, rows, or columns.
"""
NOT_ENOUGH_CLUES = """
You have provided fewer than 17 clues. Note that, while this puzzle
might still be solvable, the solution may not be unique. To have a
unique solution, you need to provide at least 17 correct clues.
"""


class SudokuSolver:
    """
    A sudoku solver.
    """

    def __init__(self, puzzle: list[list]) -> None:
        if isinstance(puzzle, tuple):
            self.puzzle = list(puzzle)
        else:
            self.puzzle = puzzle

    def _print_sudoku(self, puzzle: list[list]) -> None:
        """
        Helper function to print the sudoku.
        Called by the solveSudoku function.
        """
        print()
        for idx, row in enumerate(puzzle):
            toprint = f" {row[0]}  {row[1]}  {row[2]}  |  {row[3]}  {row[4]}  {row[5]}  |  {row[6]}  {row[7]}  {row[8]}"
            print(toprint)
            if idx == 2 or idx == 5:
                print('-' * len(toprint))
        return

    def isRightType(self, type_tuple: tuple, idx1: int, idx2=None) -> bool:
        """
        Helper function to check if contents of the puzzle are of the
        right type and length:
            - rows can be either lists, tuples or strings of length 9.
                - if they are tuples/strings, we convert to lists.
            - cells can be either strings or integers in range(10).
                - if they are strings and numeric, we convert to integers.

        Called by the isValidSudoku function.

        Takes as input:
            - type_tuple -> a tuple of length 2 where the first element is
                the desired type and the second element is the acceptable type
                or a tuple of acceptable types.
            - idx1 -> index of the row we're considering.
            - idx2 -> index of the cell we're considering.
                Set to None if we're only checking a row.

        Returns a boolean indicating whether or not the content is of the
        right type.
        """
        
        desired_type, acceptable_type = type_tuple
        puzzle_item = self.puzzle[idx1] if idx2 is None else self.puzzle[idx1][idx2]
        if not isinstance(puzzle_item, desired_type):
            if isinstance(puzzle_item, acceptable_type):

                if idx2 is None:
                    self.puzzle[idx1] = desired_type(puzzle_item)
                    return len(puzzle_item) == 9
                else:
                    try:
                        # This is needed for when we're trying to convert strings to integer.
                        # It could be that we're trying to convert something that isn't numeric.
                        self.puzzle[idx1][idx2] = desired_type(puzzle_item)
                    except ValueError:
                        return False
                    # Ensure cell entries are in range(10).
                    return 0 <= self.puzzle[idx1][idx2] <= 9
            # Wasn't of the right type.
            return False
        if idx2 is None:
            # Ensure rows are of length 9.
            return len(puzzle_item) == 9
        # Ensure cell entries are in range(10).
        return 0 <= self.puzzle[idx1][idx2] <= 9

    def isValidSudoku(self) -> bool:
        """
        Helper function to check if the given
        puzzle is 'valid'. Called by the
        solveSudoku function.

        The validity checks: 
            - the sudoku is a 9 x 9 grid,
            - outer container is a list or tuple,
            - inner containers are lists/tuples/strings, 
            - cell entries are in range(10).

        Returns boolean indicating if the sudoku is
        valid or not. 
        """

        # We permit tuples instead of lists for the puzzle.
        # In such a case, we transform the puzzle into a list.
        # Note that this transformation has already been done
        # in the init function.
        if not isinstance(self.puzzle, list):
            print("Not a valid 9 X 9 sudoku. It should be either a list or tuple.")
            return False

        if len(self.puzzle) != 9:
            print("Not a valid 9 X 9 sudoku. It should be a 9 x 9 grid.")
            return False

        for row_index in range(9):
            # We permit tuples or strings instead of lists for the rows.
            if not self.isRightType((list, (tuple, str)), row_index):
                print(
                    "Not a valid 9 X 9 sudoku. Rows should be only lists, tuples or strings of length 9.")
                return False

            for entry_index in range(9):
                # We also permit ints masked as strs for the cell entries.
                if not self.isRightType((int, str), row_index, entry_index):
                    print(
                        "Not a valid 9 X 9 sudoku. All cell entries should be numerics in range(10).")
                    return False

        # All checks are fine.
        return True

    def solveSudoku(self):
        """
        Main function.
        Takes as input, a 9 x 9 sudoku represented
        as a list of lists.

        If solved successfully, it prints out the solved puzzle,
        else, it prints an appropriate message.

        Returns boolean indicating whether or not the puzzle
        was solved successfully.

        In the case where the puzzle was found to be invalid
        due to type inconsistencies, it returns None.
        """

        # We do a validity check on the puzzle.
        if not self.isValidSudoku():
            # The puzzle is not valid. The appropriate message
            # has been printed. We quit the program here.
            return None

        # We use the _print_sudoku function to print
        # our puzzle with one modification: We set empty
        # cells to '*' just to make it easier to see
        # what we know and what we don't.
        self._print_sudoku([['*' if num == 0 else num for num in row]
                           for row in self.puzzle])

        # We collect all empty cells in one place.
        # This list is what we will use to recursively solve
        # the sudoku.
        allzeros = [(i, k) for i in range(9)
                    for k in range(9) if self.puzzle[i][k] == 0]

        # No point solving a "solved" puzzle.
        if not allzeros:
            print("Puzzle has no zero entry.")
            return None

        # To be guaranteed a unique solution, the sudoku should have
        # at least 17 clues correctly placed (or put another way, it
        # should have at most 64 empty cells). If this is not the case
        # we print an appropriate message and go on to attempt to
        # solve the puzzle.
        if len(allzeros) > 64:
            print(NOT_ENOUGH_CLUES)

        # We call the recursiveSolveSudoku function to solve
        # the sudoku.
        if self.recursiveSolveSudoku(allzeros):
            # If we were able to solve the sudoku, we return True
            # and print it out nicely with the _print_sudoku function.
            #
            # For the sake of testing, we also return the solved puzzle
            # as a list of strings (each row is combined into a string).
            self._print_sudoku(self.puzzle)
            return True, [''.join(str(itm) for itm in row) for row in self.puzzle]

        else:
            print(PUZZLE_NOT_SOLVABLE)
            return False

    def recursiveSolveSudoku(self, allzeros: list[tuple], pos=0) -> bool:
        """
        The recursive solver for the sudoku.
        It takes two inputs: 
            - allzeros -> the list of all empty cells in the puzzle, and
            - pos -> integer indicating which empty cell we are checking.

        It returns one output:
            - a boolean indicating whether or not we were able to solve
                the sudoku.
        """

        if pos == len(allzeros):
            # We've successfully processed all empty cells.
            # This means we have a valid solution.
            return True

        row, col = allzeros[pos]

        # We generate the 3 x 3 sub-grid containing the current empty cell.
        grid = [self.puzzle[row - row % 3 + i][col - col % 3 + j]
                for i in range(3)
                for j in range(3)]

        # A list of possible values for this position.
        # We generate this list by eliminating all numbers in the range(1, 10)
        # currently in
        #   - the 3 x 3 grid,
        #   - the row containing this cell, and
        #   - the column containing this cell.
        not_in = [j for j in range(1, 10)
                  if not j in self.puzzle[row] and
                  not j in [self.puzzle[k][col] for k in range(9)] and
                  not j in grid]

        ind = 0
        while ind < len(not_in):
            # We progressively work through all possible values for the
            # position by doing the following:
            #   - take a value from the not_in list,
            #   - set the current position in the puzzle to be this value,
            #   - increment pos (that is, move to the next empty cell)
            #   - if this doesn't work, backtrack (that is, decrement pos
            #       and reset the current position to be zero again),
            #       take the next possible value and go back to step 2.
            #   - Else, return the solution.
            #
            # Observe that "works" here means we're able to fill in
            # values for every empty cell starting from this position
            # with this choice, and "doesn't work" means, for some empty
            # cell further ahead, we're unable to find a possible value,
            # i.e, the not_in list turns out to be empty.

            possible_value = not_in[ind]
            self.puzzle[row][col] = possible_value
            pos += 1
            trial = self.recursiveSolveSudoku(allzeros, pos)
            if not trial:
                self.puzzle[row][col] = 0
                pos -= 1
                ind += 1
            else:
                return trial

        # We couldn't find a value that works.
        return False


if __name__ == '__main__':
    # More example sudokus can be found in test_solver.py

    # Valid and solvable.
    solvable_puzzle1 = (
        (0, 0, 6, '0', 0, 7, 3, 0, 0),
        [0, 0, 1, 0, 0, 0, 0, 4, 0],
        [0, 0, 0, 4, 2, 0, 0, 5, 0],
        [0, 7, 0, 9, 0, 5, 0, 0, 0],
        [0, 2, 5, 6, 0, 0, 0, 0, 0],
        [9, 0, 0, 0, 0, 0, 8, 0, 0],
        [0, 8, 0, 0, 0, 4, 0, 3, 0],
        [7, 0, 0, 0, 9, 0, 0, 6, 0],
        [0, 0, 0, '3', 0, 2, 4, 0, 0]
    )

    import time
    start = time.perf_counter()
    sudoku = SudokuSolver(solvable_puzzle1)
    solved_sudoku = sudoku.solveSudoku()
    end = time.perf_counter()

    if solved_sudoku:
        print()
        print(f"It took {round(end - start, 3)}s to solve this puzzle.")
    elif solved_sudoku == False:
        print(
            f"It took {round(end - start, 3)}s to determine there's no solution for this puzzle.")
