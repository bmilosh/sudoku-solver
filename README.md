# Sudoku Solver
A sudoku solver that doubles as a game. **GUI for game added!!! To play, run `play_game_gui.py`**
## Description
With this program, you can solve any correctly written `9 x 9` sudoku. Surprisingly (double wink), you can also play a game or two of sudoku with it.
## How The Solver Works
1. Create an instance of the `SudokuSolver` with your puzzle as input (acceptable input formats will be discussed in the next section).
2. Call the `solveSudoku` method on your `SudokuSolver` instance.
3. The `solveSudoku` method performs a number of validity checks on your puzzle (discussed in the next section).
4. If all checks are satisfied, it goes ahead to print your puzzle as a `9 x 9` grid with empty cells represented as `'*'`.
5. Your puzzle is passed to the `recursiveSolveSudoku` method which is the method that actually solves your sudoku.
6. If a solution is found, it is printed as a `9 x 9` grid. Otherwise, an appropriate message is printed.
## Input Types and Validity Checks
A number of input types are accepted for the puzzle:
1. Your puzzle can be a `list` or a `tuple`.
2. Rows can be any of the following:
    * `list` of `integers`/`strings`,
    * `tuple` of `integers`/`strings`,
    * Numeric `strings`.

When you call the `solveSudoku`method, it checks that your puzzle and its elements all have the appropriate types.
An additional validity check it does is to ensure that you have a `9 x 9` sudoku. To do this, it checks the lengths of the puzzle and its rows.

If any of the validity checks fails, a message is printed indicating what happened and the program exits.
## How The Game Works
Unfortunately, there's no GUI to play the game for now (yeah, sad, I know) so you'll have to play from your terminal. Still fun but slightly more tedious. Asides that, playing the game is rather straightforward. Just 
1. Create an instance of `PlaySudoku` in `play_game.py`.
2. Call `playGame` on that instance.
3. Run `play_game.py` in your terminal.
4. Play to your heart's fill.

I tried to make the game as interactive as possible, so you'll find prompts for almost everything. Messages are as descriptive as possible, I think. However, it's definitely not perfect. Hence, comments and contributions will be appreciated.

As with any game, once you start, all prompts for user input are persistent. However, you can gracefully exit anytime with a `KeyboardInterrupt` (i.e., by doing `CTRL-C` on Windows and `CMD-C`, I think, on Mac).
## To-Do
- [x] Add a way to randomly generate sudokus. Currently, the program serves to solve the user's sudoku. It can be extended to also give the user something to solve.
- [x] Add a user interface. 
- [x] Add a graphical user interface. 
- [ ] Add a web interface. This will be nice to have, but...
