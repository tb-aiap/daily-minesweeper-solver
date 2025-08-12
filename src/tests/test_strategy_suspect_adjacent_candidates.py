"""Test file for suspecting cells from neighbors, to test for various patterns."""

from daily_minesweeper import data_model, solver


def test_suspect_neighbors_4_1_and_empty_1():
    """Test that function update based on cells 2 square away."""
    sample_board = [
        ["", "", "", "", ""],
        ["", "", "", "", ""],
        ["", "4", "", "1", ""],
        ["", "", "", "", ""],
        ["", "", "", "", ""],
    ]
    board = solver.Board(sample_board)
    # set state
    board[1][0].state = data_model.CellState.flag
    board[2][0].state = data_model.CellState.flag

    board[1][1].state = data_model.CellState.empty
    board[1][2].state = data_model.CellState.empty
    board[1][3].state = data_model.CellState.empty
    board[3][0].state = data_model.CellState.empty

    result = solver.suspect_adjacent_candidates_and_mark_neighbor_empty(2, 1, board)
    assert result

    expected = [(3, 1)]
    for r, c in expected:
        assert board[r][c].state == data_model.CellState.flag

    expected_empty = [(2, 4), (3, 4)]
    for r, c in expected_empty:
        assert board[r][c].state == data_model.CellState.empty

    result = solver.suspect_adjacent_candidates_and_mark_neighbor_empty(2, 1, board)
    assert not result


def test_suspect_neighbors_1_1_and_empty_1():
    """Test that function update based on cells 2 square away."""
    sample_board = [
        ["1", "", "1", "0", ""],
        ["", "", "", "", ""],
        ["2", "", "", "1", ""],
        ["", "", "", "", ""],
        ["", "", "", "", ""],
    ]
    board = solver.Board(sample_board)
    # set state
    board[1][2].state = data_model.CellState.empty
    board[1][3].state = data_model.CellState.empty
    board[1][4].state = data_model.CellState.empty
    board[0][4].state = data_model.CellState.empty

    result = solver.suspect_adjacent_candidates_and_mark_neighbor_empty(0, 2, board)
    assert result

    expected_empty = [(1, 0)]
    for r, c in expected_empty:
        assert board[r][c].state == data_model.CellState.empty

    result = solver.suspect_adjacent_candidates_and_mark_neighbor_empty(0, 2, board)
    assert not result


def test_suspect_neighbors_4_2_and_empty_2():
    """Test that function update based on cells 2 square away."""
    sample_board = [
        ["", "", "", "", ""],
        ["", "", "", "", ""],
        ["4", "", "2", "", ""],
        ["", "", "", "", ""],
        ["", "", "", "", ""],
    ]
    board = solver.Board(sample_board)

    result = solver.suspect_adjacent_candidates_and_mark_neighbor_empty(2, 0, board)
    assert result

    expected = [(1, 0), (3, 0)]
    for r, c in expected:
        assert board[r][c].state == data_model.CellState.flag

    expected_empty = [(1, 2), (1, 3), (2, 3), (3, 3), (3, 2)]
    for r, c in expected_empty:
        assert board[r][c].state == data_model.CellState.empty

    result = solver.suspect_adjacent_candidates_and_mark_neighbor_empty(2, 0, board)
    assert not result
