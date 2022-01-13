

from solver import SudokuSolver
import pytest


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

# Invalid puzzle: rows are of the wrong type.
invalid_puzzle3 = (
    123456789,
    123456789,
    123456789,
    123456789,
    123456789,
    123456789,
    123456789,
    123456789,
    123456789
)

# Invalid puzzle: one row has more than 9 elements.
invalid_puzzle4 = (
    '1233456789',
    '123456789',
    '123456789',
    '123456789',
    '123456789',
    '123456789',
    '123456789',
    '123456789',
    '123456789'
)

# Invalid puzzle: contains non-numeric characters.
invalid_puzzle5 = (
    '1abcd6789',
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
    invalid_puzzle1,
    invalid_puzzle2,
    invalid_puzzle3,
    invalid_puzzle4,
    invalid_puzzle5
])
def test_invalid_puzzle(puzzle):
    assert SudokuSolver(puzzle).solveSudoku() is None


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
def test_no_zero_entry(puzzle):
    assert SudokuSolver(puzzle).solveSudoku() is None


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

# Valid in terms of types, but not solvable because
# certain entries are not correct. Replace the
# first row with [5, 3, 0, 0, 7, 0, 0, 0, 0]
# to get a solvable sudoku.
non_solvable_puzzle2 = [
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]


@pytest.mark.parametrize("puzzle", [
    non_solvable_puzzle1,
    non_solvable_puzzle2
])
def test_non_solvable_puzzle(puzzle):
    assert not SudokuSolver(puzzle).solveSudoku()


# Valid but has no unique solution as it contains
# fewer than 17 clues.
non_unique_solution1 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]


def test_non_unique_solution():
    assert SudokuSolver(non_unique_solution1).solveSudoku()


# Valid and solvable. Mixture of different acceptable types.
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

# Valid and solvable. Mixture of different acceptable types.
solvable_puzzle2 = [
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
solvable_puzzle3 = (
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

solution_to_puzzle1 = [
    '496157382',
    '251836947',
    '837429156',
    '178945623',
    '325681794',
    '964273815',
    '682714539',
    '743598261',
    '519362478'
]

solution_to_puzzle2 = [
    '145327698',
    '839654127',
    '672918543',
    '496185372',
    '218473956',
    '753296481',
    '367542819',
    '984761235',
    '521839764']

solution_to_puzzle3 = [
    '162857493',
    '534129678',
    '789643521',
    '475312986',
    '913586742',
    '628794135',
    '356478219',
    '241935867',
    '897261354'
]


@pytest.mark.parametrize("puzzle, expected_answer", [
    (solvable_puzzle1, solution_to_puzzle1),
    (solvable_puzzle2, solution_to_puzzle2),
    (solvable_puzzle3, solution_to_puzzle3)
])
def test_solvable_puzzle(puzzle, expected_answer):
    solution = SudokuSolver(puzzle).solveSudoku()
    assert len(solution) == 2 and solution[1] == expected_answer
