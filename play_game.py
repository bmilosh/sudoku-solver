import time
from random import randint, shuffle

from solver import SudokuSolver

CHOOSE_LEVEL_MESSAGE = """
Welcome to Michael's Sudoku! Hope you have a great time playing!
Please, choose the level you want. 
Type '0' for 'Easy', '1' for 'Medium' or '2' for 'Hard':"""

REMIND_PLAYER_OF_LEVEL_OPTIONS = """
You should type '0' for 'Easy', '1' for 'Medium' or '2' for 'Hard':"""

CHOOSE_CELL_MESSAGE2 = """
Please, enter a cell followed by the equals sign and a value (e.g. 'a5 = 8') and press 'enter':
Empty cells are shown with an '*'.
Rows are labelled downward from 'a' to 'i' and columns are labelled rightward from 1 to 9"""

CHOOSE_CELL_MESSAGE = """
You can restart with a fresh game by typing 'r'.
Please, enter a cell followed by the equals sign and a value (e.g. 'a5 = 8') and press 'enter':"""

ROW_AND_COLUMN_ID_MESSAGE = """
Rows are labelled downward from 'a' to 'i' and columns are labelled rightward from 1 to 9."""

COLUMN_OR_VALUE_OUT_OF_RANGE = """
Please, enter a valid column and value. Both should be integers between 1 and 9 inclusive:"""

SPOT_TAKEN_MESSAGE = """
Sorry, but that spot is taken. Please, enter a value for an empty cell:"""

NO_LEGAL_MOVES = """
There are no legal values for this cell. You need to backtrack."""

NOT_LEGAL_VALUE = """
 is not a legal value for this cell. Please, enter a legal value or choose another cell:"""

KEYBOARD_INTERRUPT_MESSAGE = """
You have chosen to end the game."""


class PlaySudoku(SudokuSolver):
    def __init__(self) -> None:
        self.levels = {'0': 'Easy',
                       '1': 'Medium',
                       '2': 'Hard'}
        # self.clues has the sense of ['Easy','Medium','Hard']
        # We randomly decide how many clues the game instance
        # will have, depending on the difficulty level. The
        # fewer the clues, the higher the difficulty level.
        # This is not true in general, but nevertheless,
        # that's the principle we use here.
        self.clues = [randint(78, 80), randint(
            30, 35), randint(23, 29)]  # randint(36, 42) randint(74, 78)

        self.puzzle = None
        self.indices = None
        self.moves_stack = None
        self.empty_cells = None
        self._generate_board()
        super().__init__()

    def _generate_board(self):
        """
        Generates the board in preparation for the game.
        Called from the start by the init function.
        Also called after each game session by the
        restartGame function.
        Necessary because we need to generate a new
        board each time the player chooses to play.
        """
        self.puzzle = [[0] * 9 for _ in range(9)]
        self.puzzle[0][0] = randint(1, 9)
        self.solveSudoku(True)

        # Used to decide which cells get set to empty before the game starts.
        # Shuffled to make it a random choice.
        self.indices = [(i, j) for i in range(9) for j in range(9)]
        shuffle(self.indices)

        # Moves made will be placed here. Needed for when the player
        # needs to undo their last move for whatever reason.
        self.moves_stack = []

        # To display the current empty cells in the sudoku.
        # Will be updated as the game progresses with
        # insertions and removals, depending on the player's
        # choice.
        self.empty_cells = []

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

        Differs from _generate_board because, among other things,
        it assumes the existence of a puzzle (which is actually
        generated by _generate_board).

        Note that we do not force the player to find the solution
        we found when generating the board. All that's important
        is that they find a valid solution for the board we
        present to them.
        """
        game_level = self.chooseLevel()

        # This is just the number of empty cells the
        # board will have. As we mentioned earlier,
        # we decide difficulty based on number of clues
        # (or empty cells) the board has.
        level = 81 - self.clues[int(game_level)]

        # Leave only the required number of empty cells.
        self.indices = self.indices[:level]
        for r, c in self.indices:
            self.puzzle[r][c] = 0

            # This looks something like 'a5'
            cell = self.row_ids[r] + str(c + 1)
            self.empty_cells.append(cell)
        self.empty_cells.sort()

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
                print("Exiting...")
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

        # We also add the cell back to the list of empty cells.
        self.empty_cells.append(row_and_col.strip().lower())
        self.empty_cells.sort()

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

    def restartGame(self):
        """
        Called after a game has been completed so as
        to immediately start another one.
        """
        print("Loading new puzzle...")
        self._generate_board()
        self.playGame()

    def _player_move(self):
        """
        Used to preprocess the player's input before passing it to
        playGame. All manner of checks are done on the input.
        It persists until the player get's it right, restarts, or
        quits.

        Called by playGame.
        """
        if self.empty_cells:
            # As long as there are empty cells, we'll display them.
            print(ROW_AND_COLUMN_ID_MESSAGE)
            print("The current empty cells are:")

            # We don't want to display more than 15 per line.
            i = 15
            empty_cells = self.empty_cells[:i]
            while empty_cells:
                print(empty_cells)
                empty_cells = self.empty_cells[i:i+15]
                i += 15
        if self.moves_stack:
            print("You can type 'u' to undo your last move.")
        print(CHOOSE_CELL_MESSAGE.strip())

        while True:
            # As long as you're with us, we'll be on
            # your neck till you get it right.
            # Let's do this.
            try:
                response = input().strip()
                if response.lower() in ['u', 'r']:
                    return response.lower()
                cell, value = response.split('=')
                cell = cell.strip()
                row = self.row_ids.index(cell[0].lower())
            except (ValueError, IndexError):
                print("Please, enter a valid cell and value.")
            except KeyboardInterrupt:
                # Fine! You don't want to play.
                # We'll go get someone else to play.
                print(KEYBOARD_INTERRUPT_MESSAGE)
                print("Exiting...")
                quit()

            else:
                # Seems you typed something that looks like what we asked for.
                # But we won't be taking any chances. We'll vet your response
                # thoroughly.
                try:
                    value = int(value.strip())
                    col = int(cell[1:])
                except (ValueError, IndexError):
                    # We don't know what you typed here, but whatever it is,
                    # it's not what we want. Behave.
                    print(COLUMN_OR_VALUE_OUT_OF_RANGE)
                    print(CHOOSE_CELL_MESSAGE)

                else:
                    if value not in range(1, 10) or len(cell) != 2 or col not in range(1, 10):
                        # Excuse you?! You know you have to enter values in range(1, 10), right?
                        # Also, your cells should be something like 'e4', not whatever it is
                        # you actually typed. -_-
                        print(COLUMN_OR_VALUE_OUT_OF_RANGE)

                    else:
                        col = col - 1
                        if self.puzzle[row][col] != 0:
                            # Hey! That spot's taken!
                            # Go find your own! -_-
                            print(SPOT_TAKEN_MESSAGE)
                            continue
                        # Yep, we need to check if your move is legal.
                        # Don't want you conning us or something. -_-
                        has_legal_moves, is_legal = self._check_legal_moves(
                            row, col, value)

                        if not has_legal_moves:
                            # Aha! You actually have no legal moves for this cell.
                            # Glad we caught that.
                            print(NO_LEGAL_MOVES)
                            return False
                        elif not is_legal:
                            # Even worse (or maybe not)! You chose an illegal value.
                            print(str(value) + ' ' + NOT_LEGAL_VALUE.strip())
                        else:
                            # It all checks out. You may proceed.
                            # Eyes on you still, though. o_o
                            return row, col, value, response, cell

    def playGame(self):
        """
        The outward-facing function that sets things in motion.
        """
        self._set_board()

        # We only want to print certain messages when it's necessary.
        last_move_legal = True

        # We only want to show the board when it's necessary.
        show_board = True
        start = time.perf_counter()
        while True:
            print(self.moves_stack)
            if not self.indices:
                # There are no more empty cells. Hurray! But wait.
                # Have you really solved the puzzle? Let's find out.
                is_complete = self._check_valid_sudoku()
                if is_complete:
                    # It appears you really did solve the puzzle. :)
                    # Good for you. Congratulations are in order.
                    # Let's show you how much time you spent.
                    end = time.perf_counter()
                    self.printSudoku(True)
                    print()
                    print("Congratulations! Sudoku solved!")
                    time_in_seconds = str(round(end - start, 2))
                    split_time = time_in_seconds.split('.')
                    if (m := int(split_time[0])) < 60:
                        print(
                            f"Time spent on this sudoku: {'.'.join(split_time)}s")
                    else:
                        print(
                            f"Time spent on this sudoku: {round(m / 60, 2)} minutes")

                    # Can we interest you in another game? Yes, of course. ;)
                    self.restartGame()
                else:
                    # I'm not sure what to do in this case.
                    # Ideally, you should go back and undo 
                    # some moves. But I'm not sure the best
                    # way to go about it. So for now, we'll
                    # just restart.
                    self.restartGame()

            if show_board:
                self._print_sudoku([['*' if num == 0 else num for num in row]
                                    for row in self.puzzle])

            if not last_move_legal:
                print()
                print("Your previous move was undone.")
            try:
                response = self._player_move()
                # Can we unpack your response? Into how many pieces?
                row, col, value, move, cell = response
            except (TypeError, ValueError):
                # It appears we can't.
                if response.lower() == 'r':
                    if self._confirm_restart():
                        # We need to confirm you really did
                        # intend to press 'r' -_-
                        self.restartGame()
                    else:
                        # Turns out it was a mistake. Phew!
                        # Glad we checked aren't you?
                        continue
                if not self.moves_stack:
                    # You either chose to undo your last move by
                    # pressing 'u' or we decided to do it for you
                    # since you actually have no legal moves for
                    # the cell you chose.

                    # In any case, the question to ask is this:
                    # How many moves can you undo?
                    last_move_legal = True
                    show_board = False
                    print("You have no moves to undo.")
                    continue
                last_move_legal = False
                show_board = True
                self._undo_last_move()

            else:
                # Let's implement and log your move...
                last_move_legal = True
                show_board = True
                self.moves_stack.append(move)
                self.puzzle[row][col] = value
                self.indices.remove((row, col))
                self.empty_cells.remove(cell)

    def _confirm_restart(self):
        """
        Called when the player types 'r' to restart a game.
        Just used to ensure the key press was intended.
        """
        print("Are you sure you want to restart with a fresh game?")
        print("You will lose all progress on this one if you do so.")
        print("Type 'yes' to confirm or press 'enter' to continue current game: ")
        while True:
            try:
                confirm = input()
            except KeyboardInterrupt:
                print(KEYBOARD_INTERRUPT_MESSAGE)
                print("Exiting...")
                quit()
            else:
                if not confirm:
                    # Catches the 'enter' key press.
                    print("Returning to current game.")
                    return False
                elif confirm.strip().lower() == 'yes':
                    print("Restarting with another game...")
                    return True
                else:
                    print(
                        "Please, type 'yes' to restart or press 'enter' to continue current game:")


if __name__ == '__main__':
    we_play = PlaySudoku()
    we_play.playGame()
