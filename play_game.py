import time
from random import randint, shuffle
from solver import SudokuSolver


CHOOSE_LEVEL_MESSAGE = """
Welcome to Michael's Sudoku! Hope you have a great time playing!
Please, choose the level you want. 
Type '0' for 'Easy', '1' for 'Medium' or '2' for 'Hard':"""

REMIND_PLAYER_OF_LEVEL_OPTIONS = """
You should type '0' for 'Easy', '1' for 'Medium' or '2' for 'Hard'."""

CHOOSE_CELL_MESSAGE = """
Please, enter a cell followed by the equals sign and a value (e.g. 'a5 = 8') and press 'enter'.
Empty cells are shown with an '*'.
Rows are labelled downward from 'a' to 'i' and columns are labelled rightward from 1 to 9"""

ROW_AND_COLUMN_ID_MESSAGE = """
Rows are labelled downward from 'a' to 'i' and columns are labelled rightward from 1 to 9"""

COLUMN_OR_VALUE_OUT_OF_RANGE = """
Please, enter a valid column and value. Both should be integers between 1 and 9 inclusive."""

SPOT_TAKEN_MESSAGE = """
Sorry, but that spot is taken. Please, enter a value for an empty cell."""

NO_LEGAL_MOVES = """
There are no legal values for this cell. You need to backtrack."""

NOT_LEGAL_VALUE = """
 is not a legal value for this cell. Please, enter a legal value."""


class GenerateSudoku(SudokuSolver):
    def __init__(self) -> None:
        self.puzzle = [[0] * 9 for _ in range(9)]
        self.puzzle[0][0] = randint(1, 9)
        self.solveSudoku(True)

        self.levels = {'0': 'Easy',
                       '1': 'Medium',
                       '2': 'Hard'}
        # self.clues has the sense of ['Easy','Medium','Hard']
        self.clues = [randint(74, 78), randint(
            30, 35), randint(23, 29)]  # randint(36, 42) randint(74, 78)
        
        # Used to decide which cells get set to empty before the game starts.
        # Shuffled to make it a random choice.
        self.indices = [(i, j) for i in range(9) for j in range(9)]
        shuffle(self.indices)

        # Moves made will be placed here. Needed for when the player
        # needs to undo their last move when they no longer have a
        # legal move for some cell.
        self.moves_stack = []
        super().__init__(self.puzzle)

    def generateSudoku(self) -> list[list]:
        return self.puzzle

    def _set_board(self):
        """
        Used to prepare the board for the game.
        Called only once per session by the playGame function.
        Depending on the difficulty level chosen by the player,
        we set a random number of cells in the board to be
        empty. These are the cells the player needs to fill
        correctly to complete the game.

        Note that we do not force the player to find the solution
        we found when generating the board. All that's important
        is that they find a valid solution for the board we
        present to them.
        """
        game_level = self.chooseLevel()
        level = 81 - self.clues[int(game_level)]
        self.indices = self.indices[:level]
        for r, c in self.indices:
            self.puzzle[r][c] = 0

    def chooseLevel(self) -> str:
        """
        Prompt for the player to choose the level
        of difficulty they want.
        It also displays a welcome message.
        Called only once per session by the _set_board function.
        """
        print(CHOOSE_LEVEL_MESSAGE)
        while True:
            try:
                level_id = input().strip()
                game_level = self.levels[level_id]
            except KeyError:
                print(REMIND_PLAYER_OF_LEVEL_OPTIONS)
            except KeyboardInterrupt:
                print("You have chosen to end the game. Goodbye.")
                quit()
            else:
                print(f"Your chosen level: {game_level}.")
                break
        return level_id

    def _undo_last_move(self):
        """
        Undoes the last move made by the player.
        Called automatically when the player chooses
        a cell for which they no longer have legal
        moves. Can also be called by the player to
        undo a move (they do this by typing 'u').

        It takes for granted that it'll only be called
        when there's in fact a move to undo, so no checks
        are made here.
        """
        print(f"Your last move '{self.moves_stack[-1]}' has been undone.")
        move = self.moves_stack.pop()
        row_and_col, _ = move.split('=')
        row = self.row_ids.index(row_and_col[0].strip().lower())
        col = int(row_and_col[1].strip()) - 1
        self.puzzle[row][col] = 0
        # We add the cell index back to the list of empty cells.
        self.indices.append((row, col))

    def _check_legal_moves(self, row: int, col: int, value: int) -> bool:
        """
        Used to verify the validity of a move.
        Called by the _player_move function.
        
        Takes as input:
            - row -> row index of the cell
            - column -> column index of the cell
            - value -> player's choice to fill the cell
        
        Returns two booleans. One indicating if there are
        legal moves for the chosen cell, and another if the
        proposed value is legal for the cell.
        """
        grid = [self.puzzle[row - row % 3 + i][col - col % 3 + j]
                for i in range(3)
                for j in range(3)]

        not_in = [j for j in range(1, 10)
                  if j not in self.puzzle[row] and
                  j not in [self.puzzle[k][col] for k in range(9)] and
                  j not in grid]
        return not not not_in, value in not_in

    def _check_valid_sudoku(self) -> bool:
        """
        Used to confirm that the player has correctly
        solved the sudoku.
        Called by the playGame function when there
        are no more empty cells.
        Returns boolean indicating whether or not sudoku
        has been correctly solved.
        """
        return all(len(row) == len(set(row)) for row in self.puzzle)

    def _player_move(self):
        print(CHOOSE_CELL_MESSAGE)
        # print(ROW_AND_COLUMN_ID_MESSAGE)
        if self.moves_stack:
            print("You can type 'u' to undo your last move.")
        while True:
            try:
                response = input().strip()
                if response.lower() == 'u':
                    return False
                cell, value = response.split('=')
                cell = cell.strip()
                row = self.row_ids.index(cell[0].lower())
            except (ValueError, IndexError):
                print("Please, enter a valid cell and value.")
            except KeyboardInterrupt:
                print("You have chosen to end the game. Goodbye.")
                quit()
            else:
                try:
                    value = int(value.strip())
                    col = int(cell[1:])
                except (ValueError, IndexError):
                    print(COLUMN_OR_VALUE_OUT_OF_RANGE)
                    print(CHOOSE_CELL_MESSAGE)
                else:
                    if value not in range(1, 10) or len(cell) != 2 or col not in range(1, 10):
                        print(COLUMN_OR_VALUE_OUT_OF_RANGE)
                    else:
                        col = col - 1
                        if self.puzzle[row][col] != 0:
                            print(SPOT_TAKEN_MESSAGE)
                            continue
                        has_legal_moves, is_legal = self._check_legal_moves(
                            row, col, value)

                        if not has_legal_moves:
                            print(NO_LEGAL_MOVES)
                            return False
                        elif not is_legal:
                            print(str(value) + ' ' + NOT_LEGAL_VALUE.strip())
                        else:
                            return row, col, value, response

    def playGame(self):
        self._set_board()

        print(len(self.indices))
        last_move_legal = True
        show_board = True
        start = time.perf_counter()
        while True:
            print(self.moves_stack)
            if not self.indices:
                is_complete = self._check_valid_sudoku()
                if is_complete:
                    end = time.perf_counter()
                    self.printSudoku(True)
                    print("Congratulations! Sudoku solved!")
                    time_in_seconds = str(round(end - start, 2))
                    split_time = time_in_seconds.split('.')
                    if (m := int(split_time[0])) < 60:
                        print(f"Time spent: {''.join(split_time)}s")
                    else:
                        print(f"Time spent: {round(m / 60, 2)} minutes")
                    exit()
            if show_board:
                self._print_sudoku([['*' if num == 0 else num for num in row]
                                for row in self.puzzle])
            if not last_move_legal:
                print("Your previous move was undone.")
            try:
                row, col, value, move = self._player_move()
            except TypeError:
                if not self.moves_stack:
                    last_move_legal = True
                    show_board = False
                    print("You have no moves to undo.")
                    continue
                last_move_legal = False
                show_board = True
                self._undo_last_move()
            else:
                last_move_legal = True
                show_board = True
                self.moves_stack.append(move)
                self.puzzle[row][col] = value
                self.indices.remove((row, col))


if __name__ == '__main__':
    we_play = GenerateSudoku()
    we_play.playGame()
