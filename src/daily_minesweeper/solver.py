"""Modules related to solving the puzzle."""

from typing import Callable

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
                result.append((i, j))

        return result

    def get_adjacent_cell_state(
        self, row: int, col: int, state: CellState
    ) -> list[tuple[int, int]]:
        """Filters get_adjacent_cells with certain cell state."""
        neighbors = self.get_adjacent_cells(row, col)
        neighbors_w_state = [(r, c) for r, c in neighbors if self[r][c].state == state]
        return neighbors_w_state

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
    # flagged = [(r, c) for r, c in neighbors if board[r][c].state == CellState.flag]
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

    if number != 0 and number == len(unmarked) + len(flagged):
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

    # neighbors = board.get_adjacent_cells(row, col)
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


def solve_logically(
    board: Board, strategies: list[Callable[[int, int, Board], bool]]
) -> None:
    """Loop through each solving strategy on the board and try to clear as much as possible."""
    number_cells = [
        (r, c)
        for r in range(board.rows)
        for c in range(board.columns)
        if board[r][c].state == CellState.is_number
    ]

    def step() -> bool:
        """Continuously loop all strategies to apply. Stops when none of the strategy works further."""
        return any(
            strategy(r, c, board) for strategy in strategies for r, c in number_cells
        )

    while step():
        print("finish step")
        board.print_state()
        pass


if __name__ == "__main__":
    sample_board = [
        ["1", "", "1", "", ""],
        ["", "", "", "1", ""],
        ["1", "", "0", "", ""],
        ["1", "", "1", "2", ""],
        ["1", "", "", "", ""],
    ]
    board = Board(sample_board)
    print(board)
    board.print_state()

    solve_logically(board, [flag_all_numbers, flag_remaining_unmarked])

    print(board)
    board.print_state()
