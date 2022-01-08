# Sudoku Solver
A sudoku solver.
## Description
With this program, you can solve any correctly written `9 x 9` sudoku.
## How it works
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
## To-Do
1. Add a way to randomly generate sudokus. Currently, the program serves to solve the user's sudoku. It can be extended to also give the user something to solve.
2. Add a user interface. This will be nice to have, but...