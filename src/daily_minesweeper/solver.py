"""Modules related to solving the puzzle."""

from collections import defaultdict
from .data_model import Cell, CellState


class Board:
    """Board class to store the minesweeper data and includes methods to search within the board."""

    def __init__(self, initial_map: list[list[str]]) -> None:
        """Initialization to set board and dimensions."""
        self.rows = len(initial_map)
        self.columns = len(initial_map[0])
        self.board = self.initialize_board(initial_map)

    def __getitem__(self, idx: int) -> list[Cell]:
        """Return the row index of the board."""
        return self.board[idx]

    def get_adjacent_cells(self, row: int, col: int) -> list[tuple[int, int]]:
        """Get the adjacent cell including itself based on `self.board` size.

        9 cells if in the middle.
        6 cells if at the edge but in the middle.
        4 cells if at the corner.
        """
        result = []
        max_height = min(row + 1, self.rows - 1)
        min_height = max(row - 1, 0)
        max_width = min(col + 1, self.columns - 1)
        min_width = max(col - 1, 0)

        for i in range(min_height, max_height + 1):
            for j in range(min_width, max_width + 1):
                if i == row and j == col:
                    continue
                result.append((i, j))

        return result

    def get_adjacent_cell_state(
        self, row: int, col: int, state: CellState
    ) -> list[tuple[int, int]]:
        """Filters get_adjacent_cells with certain cell state."""
        neighbors = self.get_adjacent_cells(row, col)
        neighbors_w_state = [(r, c) for r, c in neighbors if self[r][c].state == state]
        return neighbors_w_state

    def get_all_cells_by_state(self, state: CellState) -> list[Cell]:
        """Get all cells in board filtered by cell state."""
        return [
            (r, c)
            for r in range(self.rows)
            for c in range(self.columns)
            if self[r][c].state == state
        ]

    def initialize_board(self, array: list[list[str]]) -> list[list[int]]:
        """Create the board with Cell class for difference value and state."""
        board = []
        for i in range(len(array)):
            board_row = []
            for j in range(len(array[0])):
                value = self.validate_value(array[i][j])
                board_row.append(
                    Cell(
                        state=self._initial_cell_state(value),
                        value=int(value),
                        x=j,
                        y=i,
                    )
                )
            board.append(board_row)
        return board

    @staticmethod
    def validate_value(value: str) -> int:
        """Check and validate value received."""
        if value == "":
            return -1

        if value.isdigit() and len(value) == 1:
            return int(value)

        raise Exception(
            f"excepts empty str or number, receive {value=} and {len(value)=}"
        )

    @staticmethod
    def _initial_cell_state(value: int) -> CellState:
        """Set initial cell state of the board."""
        if value == -1:
            return CellState.unmarked
        return CellState.is_number

    def print_state(self) -> None:
        """Print cell state."""
        for i in range(self.rows):
            board_row = []
            for j in range(self.columns):
                if self.board[i][j].state == CellState.is_number:
                    board_row.append(self.board[i][j].value)
                else:
                    board_row.append(self.board[i][j].state.value)

            print(board_row)

    def __repr__(self) -> None:
        """Print the board value by default."""
        board = ""
        for i in range(self.rows):
            board_row = []
            for j in range(self.columns):
                val = (
                    str(self.board[i][j].value) if self.board[i][j].value >= 0 else " "
                )
                board_row.append(val)

            board += str(board_row) + "\n"

        return board


def flag_all_numbers(row: int, col: int, board: Board) -> bool:
    """Flag all numbers as long as neighbors empty space is same as number.

    If the number is flagged but there are empty spaces similar to number, it will still run.
    """
    curr: Cell = board[row][col]
    updated = False

    if curr.state != CellState.is_number:
        return False

    number = curr.value
    unmarked = board.get_adjacent_cell_state(row, col, CellState.unmarked)
    flagged = board.get_adjacent_cell_state(row, col, CellState.flag)
    if len(unmarked) == 0:
        # if there are no unmarked space, ignore it.
        return updated

    if len(flagged) and len(flagged) == number:
        # if a number (2) has 2 flagged, ignore remaining empty space.
        return updated

    if number == 0:
        for r, c in unmarked:
            board[r][c].state = CellState.empty
            updated = True

    if number != 0 and number == (len(unmarked) + len(flagged)):
        for r, c in unmarked:
            board[r][c].state = CellState.flag
            updated = True

    return updated


def flag_remaining_unmarked(row: int, col: int, board: Board) -> bool:
    """For a number, if the surrounding is flagged, update all unused cell as empty."""
    curr: Cell = board[row][col]
    updated = False

    if curr.value == 0:
        return False

    flagged = board.get_adjacent_cell_state(row, col, CellState.flag)
    unmarked = board.get_adjacent_cell_state(row, col, CellState.unmarked)

    if curr.value < len(flagged):
        raise Exception(
            f"flagged more than the value {curr.value}, flagged {len(flagged)}, on {row, col}"
        )

    if curr.value == len(flagged) and len(unmarked) > 0:
        for r, c in unmarked:
            board[r][c].state = CellState.empty
            updated = True

    return updated


def deduce_from_neighbors_and_flag(row: int, col: int, board: Board) -> bool:
    """For a number, check for common neighbors pattern and flag remaining cells.

    Try to determine the subset of both neighbors. If they overlaps or not.

    Example:
    4 - 1 pattern, safe to flag top 3.
    Deduce from neighbor 1, only 1 slot. No 1 (?) overlaps with adjacent No 4
    . . .
    . 4 .
    . 1 .
    . . .

    f f f
    ? 4 ?
    ? 1 ?
    e e e
    """
    updated = False
    curr: Cell = board[row][col]
    unmarked = board.get_adjacent_cell_state(row, col, CellState.unmarked)
    flagged = board.get_adjacent_cell_state(row, col, CellState.flag)
    neighbor_number = board.get_adjacent_cell_state(row, col, CellState.is_number)

    if len(unmarked) == 0:
        return updated

    for r, c in neighbor_number:
        neighbor_value = board[r][c].value
        neighbor_unmarked = board.get_adjacent_cell_state(r, c, CellState.unmarked)
        neighbor_flagged = board.get_adjacent_cell_state(r, c, CellState.flag)

        overlapped_cell = set(unmarked).intersection(set(neighbor_unmarked))
        to_mark = [c for c in unmarked if c not in overlapped_cell]
        to_empty = [c for c in neighbor_unmarked if c not in overlapped_cell]

        if len(to_mark) == 0 and len(to_empty) == 0:
            continue

        remaining_value = curr.value - len(flagged)
        remaining_neighbor_value = neighbor_value - len(neighbor_flagged)
        if len(to_mark) and (remaining_value - remaining_neighbor_value) == len(
            to_mark
        ):
            for mr, mc in to_mark:
                board[mr][mc].state = CellState.flag
            for nr, nc in to_empty:
                board[nr][nc].state = CellState.empty
            updated = True
            break
        elif len(to_mark) == 0 and (remaining_value - remaining_neighbor_value) == 0:
            for nr, nc in to_empty:
                board[nr][nc].state = CellState.empty
            updated = True
            break
    return updated


def suspect_adjacent_candidates_and_mark_neighbor_empty(
    row: int, col: int, board: Board
) -> bool:
    """Instead of comparing adjacent neighbors, check if adjacent unmarked is used by neighbors.

    Example:
    4 - 2 pattern, but 2 is not adjacent neighbor.
    Deduce that 2 is required for 4, mark No 2 other value as empty.

    2 3 1
    . 4 .
    . . .
    . 2 .
    . . .

    Mark cell of 2 that must be empty to satisfy #4 condition
    2 3 1
    . 4 .
    . . .
    e 2 e
    e e e
    """
    updated = False
    curr: Cell = board[row][col]
    unmarked = board.get_adjacent_cell_state(row, col, CellState.unmarked)
    flagged = board.get_adjacent_cell_state(row, col, CellState.flag)

    # for each adjacent unmarked cell, get its other number neighbor.
    suspect_neighbor_hash = defaultdict(set)
    for r, c in unmarked:
        neighbor_num = board.get_adjacent_cell_state(r, c, CellState.is_number)
        for n in neighbor_num:
            if n == (row, col):
                continue
            suspect_neighbor_hash[n].add((r, c))

    if len(unmarked) == 0:
        return updated

    for k, v in suspect_neighbor_hash.items():
        overlapped = set(unmarked).intersection(v)
        k_value = board[k[0]][k[1]].value
        k_neighbor_unmarked = board.get_adjacent_cell_state(
            k[0], k[1], CellState.unmarked
        )
        k_neighbor_flagged = board.get_adjacent_cell_state(k[0], k[1], CellState.flag)

        to_mark = [c for c in unmarked if c not in overlapped]
        to_empty = [c for c in k_neighbor_unmarked if c not in overlapped]

        remaining_value = curr.value - len(flagged)
        remaining_neighbor_value = k_value - len(k_neighbor_flagged)

        if len(to_mark) == 0 and len(to_empty) == 0:
            continue

        if len(to_mark) and (remaining_value - remaining_neighbor_value) == len(
            to_mark
        ):
            for mr, mc in to_mark:
                board[mr][mc].state = CellState.flag
            for nr, nc in to_empty:
                board[nr][nc].state = CellState.empty
            updated = True
            break
        elif len(to_mark) == 0 and (remaining_value - remaining_neighbor_value) == 0:
            for nr, nc in to_empty:
                board[nr][nc].state = CellState.empty
            updated = True
            break

    return updated


if __name__ == "__main__":
    ...
