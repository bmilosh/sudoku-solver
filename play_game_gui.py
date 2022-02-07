import tkinter as tk
from random import randint, shuffle
from tkinter import ttk

from oop_solver import SudokuGenerator, SudokuSolver

HEIGHT = 540
WIDTH = 540
BOX_RATIO = 1/3


class SudokuGame(SudokuSolver):
    root = tk.Tk()
    root.title("Michael's Sudoku")
    root.configure(bg='#1a49c9', height=HEIGHT, width=WIDTH)
    frames = {}
    frame_indices = [range(3), range(3, 6), range(6, 9)]
    levels = ['Easy', 'Medium', 'Hard']
    CHOOSE_LEVEL = 'Choose Level'
    new_game_var = tk.StringVar(root)
    new_game_var.set(CHOOSE_LEVEL)

    clues = [randint(36, 42), randint(
        30, 35), randint(23, 29)]

    def __init__(self) -> None:
        self.moves_stack = []
        self.cells_with_str_keys = {}
        self.rows_and_cols_with_cells = {}
        self.can_append = True
        self.puzzle = []
        self.seconds_counter = 0
        super().__init__(self.puzzle)

    def __init_game(self):
        self.indices = [(r, c) for r in range(9) for c in range(9)]
        shuffle(self.indices)

    def _reset_variables(self):
        self.seconds_counter = 0
        self.can_append = True
        self.moves_stack.clear()
        self.cells_with_str_keys.clear()
        self.rows_and_cols_with_cells.clear()

    def _new_game(self, input: str):
        if hasattr(self, 'timer_running'):
            self.stop_timer(self.timer_running)
        self._reset_variables()
        sudoku = SudokuGenerator()
        sudoku.generateSudoku()
        self.puzzle = sudoku.puzzle

        self.__init_game()

        no_of_clues = 81 - self.clues[self.levels.index(input)]
        self.indices = self.indices[:no_of_clues]
        for row, col in self.indices:
            self.puzzle[row][col] = 0

        self.new_game_var.set(self.CHOOSE_LEVEL)

        self._add_widgets()
        self.difficulty_level_label.configure(text=input)

        self.tick()

    def _undo_move(self):
        if self.moves_stack:
            row, col, previous_value = self.moves_stack.pop()

            # Don't append to the moves_stack what we've just
            # inserted here. We won't be doing a 'redo' so
            # it's not necessary. Also, it breaks the undo
            # functionality.
            self.can_append = False
            self.rows_and_cols_with_cells[(row, col)].delete(0, 'end')
            if previous_value:
                self.rows_and_cols_with_cells[(row, col)].insert(
                    'end', previous_value)
            self.can_append = True

    def _reset_board(self):
        self.moves_stack.clear()
        if hasattr(self, 'indices'):
            for row, col in self.indices:
                self.puzzle[row][col] = 0
                self.rows_and_cols_with_cells[(row, col)].delete(0, 'end')

    def _solve_board(self):
        if hasattr(self, 'timer_running'):
            self.stop_timer(self.timer_running)
            self.seconds_counter = 0
        self.tick()
        self.solveSudoku()

        # This doesn't yet work as intended.
        self.stop_timer(self.timer_running)

    def _get_legal_values(self, row: int, col: int) -> list:
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
                  if j not in self.puzzle[row] and
                  j not in [self.puzzle[k][col] for k in range(9)] and
                  j not in grid]
        return not_in

    def _validate_entry_input(self, *args):
        if len(args) == 1:
            return True
        input, widget_and_inds = args
        widget, row_col = self.cells_with_str_keys[widget_and_inds]
        r, c = row_col

        if not input:
            # Like a backspace key press
            widget.delete(0, 'end')
            self.puzzle[r][c] = 0
            return True
        try:
            # Enables us show the single-digit integer the user just typed.
            value = int(input[-1])
        except ValueError:
            return False
        else:
            if value in range(1, 10):
                str_val = str(value)
                current_val = widget.get()
                if str_val == current_val:
                    return False
                widget.delete(0, 'end')
                not_in = self._get_legal_values(r, c)
                self.puzzle[r][c] = value
                widget.insert(0, str_val)
                if self.can_append:
                    self.moves_stack.append((r, c, current_val))

                if value in not_in:
                    widget.configure(foreground='purple')
                    return True
                else:
                    widget.configure(foreground='red')
                    return True
            else:
                return False

    def tick(self):
        self.seconds_counter += 1
        seconds = self.seconds_counter % 60
        seconds = str(seconds) if seconds >= 10 else f"0{seconds}"
        minutes = self.seconds_counter // 60
        minutes = str(minutes) if minutes else ''
        self.timer_running = self.timer.after(1000, self.tick)
        self.timer.configure(text=f'{minutes}:{seconds}')

    def stop_timer(self, id: str):
        self.timer.after_cancel(id)

    def _add_buttons(self):
        self.timer = tk.Label(self.root, text=':00',
                              font=('Arial', 12, 'bold'),)
        self.timer.place(relx=0.56, rely=0.03, relwidth=0.19, relheight=0.06)

        self.difficulty_level_label = tk.Label(self.root, font=('Arial', 12, 'bold'),
                                               justify='center', background='white',
                                               highlightbackground="black", highlightcolor="black",
                                               highlightthickness=1, relief='sunken')
        self.difficulty_level_label.place(
            relx=0.8, rely=0.2, relwidth=0.15, relheight=0.05)

        undo_move_button = tk.Button(self.root, text="Undo", font=('Arial', 12, 'bold'), relief='solid',
                                     highlightbackground="black", highlightcolor="black",
                                     highlightthickness=1, command=self._undo_move)
        undo_move_button.place(relx=0.25, rely=0.03,
                               relwidth=0.1, relheight=0.06)

        solution_button = tk.Button(self.root, text="Solution", font=('Arial', 12, 'bold'), relief='solid',
                                    highlightbackground="black", highlightcolor="black",
                                    highlightthickness=1, command=self._solve_board)
        solution_button.place(relx=0.78, rely=0.3, relwidth=0.2, relheight=0.1)

        reset_board_button = tk.Button(self.root, text="Reset Board", font=('Arial', 12, 'bold'),
                                       relief='solid', highlightbackground="black",
                                       highlightcolor="black", highlightthickness=1, command=self._reset_board)
        reset_board_button.place(
            relx=0.78, rely=0.5, relwidth=0.2, relheight=0.1)

        new_game_options = tk.OptionMenu(
            self.root, self.new_game_var, *self.levels, command=self._new_game)
        new_game_options.configure(font=('Arial', 10, 'bold'))
        new_game_options.place(relx=0.78, rely=0.1,
                               relwidth=0.2, relheight=0.1)

    def _add_frames(self):
        self.sudoku_frame = tk.Frame(self.root, bg='white', highlightbackground="black",
                                     highlightcolor="black", highlightthickness=1)
        self.sudoku_frame.place(relx=0.25, rely=0.1,
                                relwidth=0.5, relheight=0.5)

        for i in range(3):
            for j in range(3):
                frame = tk.Frame(self.sudoku_frame, bg='white', highlightbackground="black",
                                 highlightcolor="black", highlightthickness=1)
                frame.place(relx=j*BOX_RATIO, rely=i*BOX_RATIO,
                            relwidth=BOX_RATIO, relheight=BOX_RATIO)
                self.frames[(i, j)] = frame

    def _add_widgets(self, puzzle=None):
        if puzzle is None:
            puzzle = self.puzzle
        for r in range(9):
            for c in range(9):
                value = puzzle[r][c]
                for idx, itm in enumerate(self.frame_indices):
                    if r in itm:
                        frame_row_index = idx
                    if c in itm:
                        frame_col_index = idx

                if value:
                    cell = tk.Label(self.frames[(frame_row_index, frame_col_index)], text=value,
                                    font=('Arial', 15), justify='center', background='grey')
                else:
                    cell = ttk.Entry(self.frames[(frame_row_index, frame_col_index)],
                                     font=('Arial', 15), justify='center', background='grey')

                    registered_callback = self.root.register(
                        self._validate_entry_input)
                    cell.configure(validate='key', validatecommand=(
                        registered_callback, '%P', '%W'), exportselection=False)

                self.rows_and_cols_with_cells[(r, c)] = cell
                self.cells_with_str_keys[str(cell)] = (cell, (r, c))
                cell.place(relx=(c % 3)*BOX_RATIO, rely=(r % 3) *
                           BOX_RATIO, relwidth=BOX_RATIO, relheight=BOX_RATIO)

    def _recursiveSolveSudoku(self, allzeros: list[tuple], pos=0) -> bool:
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

        # A list of possible values for this position.
        not_in = self._get_legal_values(row, col)

        shuffle(not_in)

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
            self.root.update_idletasks()
            self.rows_and_cols_with_cells[(row, col)].delete(0, 'end')
            # rows_and_cols_with_cells[(row, col)].configure(foreground='orange')
            self.rows_and_cols_with_cells[(row, col)].insert(
                0, str(possible_value))
            self.puzzle[row][col] = possible_value
            pos += 1
            trial = self._recursiveSolveSudoku(allzeros, pos)
            if not trial:
                self.root.update_idletasks()
                self.rows_and_cols_with_cells[(
                    row, col)].configure(foreground='red')
                self.puzzle[row][col] = 0
                pos -= 1
                ind += 1
            else:
                return trial

        # We couldn't find a value that works.
        return False

    def play(self):
        self._add_buttons()
        self._add_frames()
        self.root.mainloop()


if __name__ == '__main__':
    game = SudokuGame()
    game.play()
