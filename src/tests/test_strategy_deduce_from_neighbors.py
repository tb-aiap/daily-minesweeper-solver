"""Test file for deduce from neighbors, to test for various patterns."""

from daily_minesweeper import data_model, solver


def test_deduce_from_neighbors_and_flag_4_1():
    """Test that function returns true, and update remaining unmarked cells accordingly."""
    sample_board = [
        ["", "", "", "", ""],
        ["", "", "4", "", ""],
        ["", "", "1", "", ""],
        ["", "", "", "", ""],
        ["", "", "", "", ""],
    ]
    board = solver.Board(sample_board)

    result = solver.deduce_from_neighbors_and_flag(1, 2, board)
    assert result

    expected = [(0, 1), (0, 2), (0, 3)]
    for r, c in expected:
        assert board[r][c].state == data_model.CellState.flag

    expected_empty = [(3, 1), (3, 2), (3, 3)]
    for r, c in expected_empty:
        assert board[r][c].state == data_model.CellState.empty

    result = solver.deduce_from_neighbors_and_flag(1, 2, board)
    assert not result


def test_deduce_from_neighbors_and_flag_5_2():
    """Test that function returns true, and update remaining unmarked cells accordingly."""
    sample_board = [
        ["", "", "", "", ""],
        ["", "", "5", "", ""],
        ["", "", "2", "", ""],
        ["", "", "", "", ""],
        ["", "", "", "", ""],
    ]
    board = solver.Board(sample_board)

    result = solver.deduce_from_neighbors_and_flag(1, 2, board)
    assert result

    expected = [(0, 1), (0, 2), (0, 3)]
    for r, c in expected:
        assert board[r][c].state == data_model.CellState.flag

    expected_empty = [(3, 1), (3, 2), (3, 3)]
    for r, c in expected_empty:
        assert board[r][c].state == data_model.CellState.empty

    result = solver.deduce_from_neighbors_and_flag(1, 2, board)
    assert not result


def test_deduce_from_neighbors_and_flag_5_3():
    """Test that function returns true, and update remaining unmarked cells accordingly."""
    sample_board = [
        ["", "", "", "", ""],
        ["", "", "5", "", ""],
        ["", "", "3", "", ""],
        ["", "", "", "", ""],
        ["", "", "", "", ""],
    ]
    board = solver.Board(sample_board)
    # set state
    board[0][1].state = data_model.CellState.empty

    result = solver.deduce_from_neighbors_and_flag(1, 2, board)
    assert result

    expected = [(0, 2), (0, 3)]
    for r, c in expected:
        assert board[r][c].state == data_model.CellState.flag

    expected_empty = [(3, 1), (3, 2), (3, 3)]
    for r, c in expected_empty:
        assert board[r][c].state == data_model.CellState.empty

    result = solver.deduce_from_neighbors_and_flag(1, 2, board)
    assert not result


def test_deduce_from_neighbors_and_flag_3_1():
    """Test that function returns true, and update remaining unmarked cells accordingly."""
    sample_board = [
        ["", "", "", "", ""],
        ["", "1", "", "", ""],
        ["", "1", "3", "", ""],
        ["", "", "", "3", ""],
        ["", "", "", "", ""],
    ]
    board = solver.Board(sample_board)

    result = solver.deduce_from_neighbors_and_flag(2, 2, board)
    assert result

    expected = [(1, 3), (2, 3)]
    for r, c in expected:
        assert board[r][c].state == data_model.CellState.flag

    expected_empty = [(1, 0), (2, 0), (3, 0)]
    for r, c in expected_empty:
        assert board[r][c].state == data_model.CellState.empty


def test_deduce_from_neighbors_and_flag_2_1_triangle():
    """Test that function returns true, and update remaining unmarked cells accordingly."""
    sample_board = [
        ["", "", "", "", ""],
        ["", "", "1", "1", ""],
        ["", "1", "2", "1", ""],
        ["", "", "", "", ""],
        ["", "", "", "", ""],
    ]
    board = solver.Board(sample_board)

    result = solver.deduce_from_neighbors_and_flag(2, 2, board)
    assert result

    expected = [(3, 3)]
    for r, c in expected:
        assert board[r][c].state == data_model.CellState.flag


def test_deduce_from_neighbors_and_flag_3_2_triangle():
    """Test that function returns false."""
    sample_board = [
        ["", "", "", "", ""],
        ["", "2", "", "2", ""],
        ["", "", "3", "4", ""],
        ["", "", "", "3", ""],
        ["", "", "", "", ""],
    ]
    board = solver.Board(sample_board)
    # set state
    board[3][2].state = data_model.CellState.flag
    board[3][4].state = data_model.CellState.flag

    result = solver.deduce_from_neighbors_and_flag(2, 2, board)
    assert not result


def test_deduce_from_neighbors_and_flag_3_2_with_1_flag_on_2():
    """Test that function returns true, and update remaining unmarked cells accordingly."""
    sample_board = [
        ["", "", "", "", ""],
        ["", "", "", "2", ""],
        ["", "", "3", "", ""],
        ["", "", "2", "", ""],
        ["", "", "", "", ""],
    ]
    board = solver.Board(sample_board)
    # set state
    board[4][2].state = data_model.CellState.flag

    result = solver.deduce_from_neighbors_and_flag(2, 2, board)
    assert result

    expected = [(1, 1), (1, 2)]
    for r, c in expected:
        assert board[r][c].state == data_model.CellState.flag
        assert board[r][c].state == data_model.CellState.flag


def test_deduce_from_neighbors_and_2_2_mark_empty():
    """Test that function returns true, and update remaining unmarked cells accordingly."""
    sample_board = [
        ["", "", "", "", ""],
        ["", "", "", "2", "2"],
        ["", "", "", "", ""],
        ["", "", "", "", ""],
        ["", "", "", "", ""],
    ]
    board = solver.Board(sample_board)

    result = solver.deduce_from_neighbors_and_flag(1, 4, board)
    assert result

    expected = [(0, 2), (1, 2), (2, 2)]
    for r, c in expected:
        assert board[r][c].state == data_model.CellState.empty


def test_deduce_from_neighbors_and_3_3_mark_empty():
    """Test that function returns true, and update remaining unmarked cells accordingly."""
    sample_board = [
        ["", "", "", "", ""],
        ["", "", "", "", ""],
        ["", "", "", "", ""],
        ["", "", "3", "", ""],
        ["", "", "3", "", ""],
    ]
    board = solver.Board(sample_board)

    result = solver.deduce_from_neighbors_and_flag(3, 2, board)
    assert not result

    result = solver.deduce_from_neighbors_and_flag(4, 2, board)
    assert result

    expected = [(2, 1), (2, 2), (2, 3)]
    for r, c in expected:
        assert board[r][c].state == data_model.CellState.empty
