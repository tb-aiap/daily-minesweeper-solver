"""Module for testing solver module."""

import pytest

from daily_minesweeper import data_model, solver


@pytest.fixture
def sample_easy_board():
    """Sample easy board for testing."""
    return [
        ["2", "", "", "", "1"],
        ["", "", "3", "2", ""],
        ["2", "", "3", "", ""],
        ["2", "", "2", "3", ""],
        ["", "", "", "", ""],
    ]


def test_validate_value():
    """Test validate function for valid numbers from html."""
    solver.Board.validate_value("")
    solver.Board.validate_value("1")

    with pytest.raises(Exception):
        solver.Board.validate_value("12")


def test_initialize_board(sample_easy_board):
    """Test initialization of minesweeper board."""
    board = solver.Board(initial_map=sample_easy_board)

    assert board.board[0][0].value == 2
    assert board.board[0][0].state == data_model.CellState.is_number

    assert board.board[0][1].value == -1
    assert board.board[0][1].state == data_model.CellState.unmarked


def test_get_adjacent_cells(sample_easy_board):
    """Test get adjacent cells function."""
    board = solver.Board(initial_map=sample_easy_board)

    result = board.get_adjacent_cells(*(0, 0))
    assert len(result) == 4
    assert (1, 1) in result

    result = board.get_adjacent_cells(*(2, 0))
    assert len(result) == 6
    assert (3, 1) in result

    result = board.get_adjacent_cells(*(1, 1))
    assert len(result) == 9
    assert (2, 2) in result


def test_getitem_board(sample_easy_board):
    """Test getitem dunder method."""
    board = solver.Board(initial_map=sample_easy_board)

    assert board[0][0].value == 2
    assert board[0][0].state == data_model.CellState.is_number

    assert board[0][1].value == -1
    assert board[0][1].state == data_model.CellState.unmarked


def test_setitem_board(sample_easy_board):
    """Test setitem is able to set."""
    board = solver.Board(initial_map=sample_easy_board)

    assert board[0][0].value == 2
    assert board[0][0].state == data_model.CellState.is_number

    board[0][0].state = data_model.CellState.suspect

    assert board[0][0].state == data_model.CellState.suspect


def test_flag_all_numbers():
    """Test that function returns true, and update board correctly."""
    sample_board = [
        ["3", "", "", "", "1"],
        ["", "", "3", "2", ""],
        ["2", "", "0", "", ""],
        ["2", "", "2", "3", ""],
        ["", "", "", "", ""],
    ]
    board = solver.Board(sample_board)

    expected_flag_before = [(0, 1), (1, 0), (1, 1)]
    for r, c in expected_flag_before:
        assert board[r][c].y == r
        assert board[r][c].x == c
        assert board[r][c].state == data_model.CellState.unmarked

    # first check in board (0,0)
    result = solver.flag_all_numbers(0, 0, board)
    assert result

    expected_flag = [(0, 1), (1, 0), (1, 1)]
    for r, c in expected_flag:
        assert board[r][c].y == r
        assert board[r][c].x == c
        assert board[r][c].state == data_model.CellState.flag

    ### SECOND BOARD WITH func ran twice
    second_sample_board = [
        ["3", "", "", "", "1"],
        ["", "", "3", "2", ""],
        ["2", "", "0", "", ""],
        ["2", "", "2", "3", ""],
        ["", "", "", "", ""],
    ]
    board = solver.Board(second_sample_board)

    # first check in board (2, 2)
    result = solver.flag_all_numbers(2, 2, board)
    assert result

    expected_flag = [(1, 1), (2, 1), (3, 1), (2, 3)]
    for r, c in expected_flag:
        assert board[r][c].y == r
        assert board[r][c].x == c
        assert board[r][c].state == data_model.CellState.flag

    # second check in board (3, 0)
    result = solver.flag_all_numbers(3, 0, board)
    assert result

    expected_flag = [(4, 0), (4, 1)]
    for r, c in expected_flag:
        assert board[r][c].y == r
        assert board[r][c].x == c
        assert board[r][c].state == data_model.CellState.flag
