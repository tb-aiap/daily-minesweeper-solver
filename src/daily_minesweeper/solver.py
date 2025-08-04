"""Modules related to solving the puzzle."""

from __future__ import annotations

from .data_model import Cell, CellState

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains


class Board:
    """Board class to store the minesweeper data and includes methods to search within the board."""

    def __init__(self, initial_map: list[list[str]]) -> None:
        """Initialization to set board and dimensions."""
        self.rows = len(initial_map)
        self.columns = len(initial_map[0])
        self.board = self.initialize_board(initial_map)

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

    def initialize_board(self, array: list[list[str]]) -> list[list[int]]:
        """Create the board with Cell class for difference value and state."""
        board = array
        for i in range(len(array)):
            for j in range(len(array[0])):
                value = self.validate_value(array[i][j])
                board[i][j] = Cell(
                    state=self._initial_cell_state(value),
                    value=int(value),
                    x=j,
                    y=i,
                )
        return board

    @staticmethod
    def validate_value(value: str) -> int:
        """Check and validate value received."""
        if value not in "0123456789" or len(value) > 1:
            raise Exception(
                f"excepts empty str or number, receive {value=} and {len(value)=}"
            )

        return -1 if len(value) == 0 else int(value)

    @staticmethod
    def _initial_cell_state(value: int) -> CellState:
        """Set initial cell state of the board."""
        if value == -1:
            return CellState.empty
        return CellState.is_number


if __name__ == "__main__":
    ...
