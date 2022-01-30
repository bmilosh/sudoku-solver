import pytest
import oop_solver as solver


# Invalid puzzle: outer container is a set.
invalid_puzzle1 = {
    (1, 2, 3, 4, 5, 6, 7, 8, 9),
    (1, 2, 3, 4, 5, 6, 7, 8, 0),
    (1, 2, 3, 4, 5, 6, 7, 0, 9),
    (1, 2, 3, 4, 5, 6, 0, 8, 9),
    (1, 2, 3, 4, 5, 0, 7, 8, 9),
    (1, 2, 3, 4, 0, 6, 7, 8, 9),
    (1, 2, 3, 0, 5, 6, 7, 8, 9),
    (1, 2, 0, 4, 5, 6, 7, 8, 9),
    (1, 0, 3, 4, 5, 6, 7, 8, 9)
}

# Invalid puzzle: one of the entries is a non-numeric string.
invalid_puzzle2 = [
    [7, 0, 0, 5, '', 0, 0, 0, 8],
    [0, 0, 0, 0, 0, 0, 7, 0, 2],
    [0, 2, 0, 8, 1, 7, 0, 0, 9],
    [5, 6, 2, 7, 9, 8, 1, 0, 4],
    [1, 3, 7, 0, 4, 2, 8, 9, 0],
    [0, 9, 0, 3, 5, 1, 6, 2, 7],
    [2, 7, 3, 9, 0, 0, 0, 0, 0],
    [6, 0, 9, 0, 0, 4, 0, 7, 3],
    [8, 1, 0, 2, 7, 3, 9, 5, 6]
]

# Invalid puzzle: Empty puzzle.
invalid_puzzle3 = []

# Invalid puzzle: one of the rows is a set.
invalid_puzzle4 = [
    {7, 0, 0, 5, '', 0, 0, 0, 8},
    [0, 0, 0, 0, 0, 0, 7, 0, 2],
    [0, 2, 0, 8, 1, 7, 0, 0, 9],
    [5, 6, 2, 7, 9, 8, 1, 0, 4],
    [1, 3, 7, 0, 4, 2, 8, 9, 0],
    [0, 9, 0, 3, 5, 1, 6, 2, 7],
    [2, 7, 3, 9, 0, 0, 0, 0, 0],
    [6, 0, 9, 0, 0, 4, 0, 7, 3],
    [8, 1, 0, 2, 7, 3, 9, 5, 6]
]

# Invalid puzzle: contains fewer than 9 rows.
invalid_puzzle5 = [
    (1, 2, 3, 4, 5, 6, 7, 8, 9),
    (1, 2, 3, 4, 5, 6, 7, 8, 2),
    (1, 2, 3, 4, 5, 6, 7, 2, 9),
    (1, 2, 3, 4, 5, 6, 2, 8, 9),
    (1, 2, 3, 4, 5, 2, 7, 8, 9),
    (1, 2, 3, 4, 2, 6, 7, 8, 9),
    (1, 2, 3, 2, 5, 6, 7, 8, 9),
    (1, 2, 3, 4, 5, 6, 7, 8, 9)
]

# Invalid puzzle: contains more than 9 rows.
invalid_puzzle6 = [
    (1, 2, 3, 4, 5, 6, 7, 8, 9),
    (1, 2, 3, 4, 5, 6, 7, 8, 2),
    (1, 2, 3, 4, 5, 6, 7, 2, 9),
    (1, 2, 3, 4, 5, 6, 2, 8, 9),
    (1, 2, 3, 4, 5, 2, 7, 8, 9),
    (1, 2, 3, 4, 2, 6, 7, 8, 9),
    (1, 2, 3, 4, 2, 6, 7, 8, 9),
    (1, 2, 3, 4, 2, 6, 7, 8, 9),
    (1, 2, 3, 2, 5, 6, 7, 8, 9),
    (1, 2, 3, 4, 5, 6, 7, 8, 9)
]


@pytest.mark.parametrize('puzzle', [
    invalid_puzzle1,
    invalid_puzzle2,
    invalid_puzzle3,
    invalid_puzzle4,
    invalid_puzzle5,
    invalid_puzzle6
])
def test_sudoku_validator_invalid_sudoku(puzzle):
    assert not solver.SudokuValidator(puzzle).isValid


# Valid puzzle: Mixed types
valid_puzzle1 = (
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

# Valid and solvable. Mixture of different acceptable types.
valid_puzzle2 = [
    (0, 0, 5, 3, 0, 0, 0, 0, 0),
    '800000020',
    [0, 7, 0, 0, 1, 0, 5, 0, 0],
    (4, '0', '0', '0', 0, '5', '3', 0, 0),
    [0, 1, 0, 0, 7, 0, 0, 0, 6],
    ['0', '0', '3', '2', '0', '0', '0', '8', '0'],
    [0, 6, 0, 5, 0, 0, 0, 0, 9],
    [0, 0, 4, 0, 0, 0, 0, 3, 0],
    [0, 0, 0, 0, 0, 9, 7, 0, 0]
]

# Valid and solvable.
valid_puzzle3 = (
    (1, 0, 0, 0, 0, 7, 0, 9, 0),
    (0, 3, 0, 0, 2, 0, 0, 0, 8),
    (0, 0, 9, 6, 0, 0, 5, 0, 0),
    (0, 0, 5, 3, 0, 0, 9, 0, 0),
    (0, 1, 0, 0, 8, 0, 0, 0, 2),
    (6, 0, 0, 0, 0, 4, 0, 0, 0),
    (3, 0, 0, 0, 0, 0, 0, 1, 0),
    (0, 4, 0, 0, 0, 0, 0, 0, 7),
    (0, 0, 7, 0, 0, 0, 3, 0, 0)
)


@pytest.mark.parametrize("puzzle", [
    valid_puzzle1,
    valid_puzzle2,
    valid_puzzle3
])
def test_sudoku_validator_valid_sudoku(puzzle):
    assert solver.SudokuValidator(puzzle).isValid


def test_sudoku_solver_validator_puzzle_correctly_assigned():
    puzzle = solver.SudokuSolver(valid_puzzle3)
    puzzle.solveSudoku()
    assert puzzle.validator.puzzle == puzzle.puzzle


# Valid outer container but invalid puzzle because an entry is invalid.
valid_type_tuple = (
    [7, 0, 0, 5, '', 0, 0, 0, 8],
    [0, 0, 0, 0, 0, 0, 7, 0, 2],
    [0, 2, 0, 8, 1, 7, 0, 0, 9],
    [5, 6, 2, 7, 9, 8, 1, 0, 4],
    [1, 3, 7, 0, 4, 2, 8, 9, 0],
    [0, 9, 0, 3, 5, 1, 6, 2, 7],
    [2, 7, 3, 9, 0, 0, 0, 0, 0],
    [6, 0, 9, 0, 0, 4, 0, 7, 3],
    [8, 1, 0, 2, 7, 3, 9, 5, 6]
)


def test_sudoku_validator_tuple_to_list():
    validator1 = solver.SudokuValidator(valid_type_tuple)
    validator2 = solver.SudokuSolver(valid_type_tuple)
    validator2.solveSudoku()
    assert isinstance(validator1.puzzle, list)
    assert not validator1.isValid
    assert not validator2.validator.isValid


generate_puzzle = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 7, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]


def test_solve_sudoku_generate_parameter():
    assert solver.SudokuSolver(generate_puzzle).solveSudoku(True) is None


# Puzzle without a zero entry.
# Not exactly a puzzle, is it? :)
no_zero_entry1 = [
    (1, 2, 3, 4, 5, 6, 7, 8, 9),
    (1, 2, 3, 4, 5, 6, 7, 8, 2),
    (1, 2, 3, 4, 5, 6, 7, 2, 9),
    (1, 2, 3, 4, 5, 6, 2, 8, 9),
    (1, 2, 3, 4, 5, 2, 7, 8, 9),
    (1, 2, 3, 4, 2, 6, 7, 8, 9),
    (1, 2, 3, 2, 5, 6, 7, 8, 9),
    (1, 2, 2, 4, 5, 6, 7, 8, 9),
    (1, 2, 3, 4, 5, 6, 7, 8, 9)
]

no_zero_entry2 = (
    '123456789',
    '123456789',
    '123456789',
    '123456789',
    '123456789',
    '123456789',
    '123456789',
    '123456789',
    '123456789'
)


@pytest.mark.parametrize("puzzle", [
    no_zero_entry1,
    no_zero_entry2
])
def test_sudoku_solver_no_zero_entry(puzzle):
    sudoku = solver.SudokuSolver(puzzle)
    assert sudoku.solveSudoku() is None


generate_puzzle1 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 7, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]


def test_sudoku_solver_not_enough_clues():
    sudoku = solver.SudokuSolver(generate_puzzle1).solveSudoku()
    assert sudoku


# Valid in terms of types, but not solvable because
# certain entries are not correct. Replace the
# first row with [7, 0, 0, 5, 0, 0, 0, 0, 8]
# to get a solvable sudoku.
non_solvable_puzzle1 = [
    [0, 0, 0, 0, 0, 0, 7, 0, 2],
    [0, 0, 0, 0, 0, 0, 7, 0, 2],
    [0, 2, 0, 8, 1, 7, 0, 0, 9],
    [5, 6, 2, 7, 9, 8, 1, 0, 4],
    [1, 3, 7, 0, 4, 2, 8, 9, 0],
    [0, 9, 0, 3, 5, 1, 6, 2, 7],
    [2, 7, 3, 9, 0, 0, 0, 0, 0],
    [6, 0, 9, 0, 0, 4, 0, 7, 3],
    [8, 1, 0, 2, 7, 3, 9, 5, 6]
]


def test_sudoku_solver_non_solvable_puzzle():
    sudoku = solver.SudokuSolver(non_solvable_puzzle1).solveSudoku()
    assert not sudoku


def test_sudoku_printer_no_puzzle():
    printer = solver.SudokuPrinter()
    assert printer.puzzle is None


def test_sudoku_printer_validator_is_valid_puzzle():
    sudoku = solver.SudokuPrinter()
    sudoku.printSudoku(non_solvable_puzzle1)
    assert sudoku.validator.isValid


def test_sudoku_printer_validator_not_valid_puzzle():
    sudoku = solver.SudokuPrinter()
    sudoku.printSudoku(invalid_puzzle6)
    assert not sudoku.validator.isValid


def test_sudoku_printer_replace_zeroes():
    sudoku = solver.SudokuPrinter()
    sudoku.printSudoku(non_solvable_puzzle1, True)
    assert sudoku.test_replace_zeroes_puzzle == [
        ['*' if item == 0 else item for item in row] for row in non_solvable_puzzle1]


def test_sudoku_generator():
    sudoku = solver.SudokuGenerator()
    assert sudoku.generateSudoku()
    assert not any(item == 0 for row in sudoku.puzzle for item in row)
