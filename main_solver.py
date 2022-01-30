import time

from solver import SudokuSolver

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
