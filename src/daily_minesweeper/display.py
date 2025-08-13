"""Module for updating console cli on minesweeper board state."""

import time

from rich import box
from rich.console import Console
from rich.live import Live
from rich.table import Table

from .data_model import Cell, CellState
from .solver import Board

console = Console()

MINE_ICON = [
    "⬤",
    "●",
    "💣",
    "🚩",
]


def create_cell_value(cell: Cell) -> str:
    """Update the cell according to its value and state."""
    colors = {
        0: "bright_white",
        1: "cyan",
        2: "green",
        3: "red",
        4: "blue",
        5: "magenta",
        6: "bright_cyan",
        7: "bright_black",
        8: "dark_red",
    }

    if cell.state == CellState.is_number:
        color = colors.get(cell.value)
        return f"[{color}]{cell.value}[/{color}]"

    if cell.state == CellState.flag:
        return f"[red]{MINE_ICON[0]}[/red]"

    if cell.state == CellState.suspect:
        return "[yellow]?[/yellow]"

    if cell.state == CellState.unmarked:
        return "[grey50]·[/grey50]"

    if cell.state == CellState.empty:
        return "[grey50]X[/grey50]"


def draw_board(board: Board) -> Table:
    """Draw table with board information."""
    width = board.columns
    height = board.rows

    table = Table(show_header=False, box=box.ASCII2, expand=False)

    for r in range(height):
        gather_row = []
        for c in range(width):
            cell = board[r][c]
            gather_row.append(create_cell_value(cell))

        table.add_row(*gather_row)

    return table


if __name__ == "__main__":
    from . import solver

    # fmt: off
    sample_board = [
        ['', '', '', '2', '', '', '', '', '', '', '', '', '1', '', '', '', '', '3', '', ''], 
        ['2', '', '', '', '', '2', '', '1', '', '0', '', '', '2', '', '1', '1', '', '', '', '2'], 
        ['', '', '4', '', '3', '', '', '2', '', '', '', '2', '', '', '1', '', '3', '', '', '1'], 
        ['', '', '', '', '2', '', '', '2', '1', '1', '', '', '', '', '1', '', '2', '', '2', ''], 
        ['', '1', '1', '', '', '', '1', '2', '', '', '', '2', '', '2', '', '', '', '', '3', ''], 
        ['', '1', '0', '2', '', '', '', '', '', '', '', '', '0', '1', '', '1', '', '', '', ''], 
        ['', '2', '', '', '4', '4', '', '2', '', '1', '', '', '1', '', '', '', '', '3', '4', ''], 
        ['', '', '2', '', '', '', '4', '', '', '', '', '', '', '3', '', '1', '', '', '', '2'], 
        ['3', '', '4', '', '', '', '', '3', '2', '2', '3', '', '', '', '3', '', '1', '', '', '2'], 
        ['', '', '2', '', '', '4', '', '', '', '', '', '', '4', '', '', '', '3', '', '1', '1'], 
        ['', '2', '', '', '3', '', '', '', '', '', '2', '', '', '', '', '', '', '', '', ''],
        ['0', '', '', '2', '2', '3', '', '2', '', '1', '', '2', '2', '', '', '5', '', '4', '', '1'], 
        ['1', '', '4', '', '', '', '', '', '', '1', '', '', '', '', '', '', '', '', '', ''],
        ['1', '', '', '', '2', '1', '2', '', '', '', '3', '', '', '2', '', '2', '', '4', '5', ''], 
        ['', '', '', '3', '', '', '', '', '2', '', '', '', '', '', '3', '4', '', '', '', ''], 
        ['', '', '2', '', '', '', '', '2', '', '', '0', '', '2', '', '', '3', '', '3', '3', ''], 
        ['3', '', '', '', '', '1', '1', '1', '', '', '1', '2', '', '', '3', '', '', '3', '', ''], 
        ['', '', '1', '1', '', '3', '', '2', '', '3', '', '', '3', '', '3', '3', '', '', '', '1'], 
        ['3', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '3', '3', ''], 
        ['', '', '1', '1', '', '', '3', '2', '', '4', '', '2', '1', '', '1', '', '', '', '', '']
    ]
    # fmt: on

    board = Board(sample_board)

    logical_strategy = [
        solver.flag_remaining_unmarked,
        solver.flag_all_numbers,
        solver.deduce_from_neighbors_and_flag,
    ]
    with Live(draw_board(board), console=console, refresh_per_second=4) as live:
        number_cells = [
            (r, c)
            for r in range(board.rows)
            for c in range(board.columns)
            if board[r][c].state == CellState.is_number
        ]

        def step() -> bool:
            """Continuously loop all strategies to apply. Stops when none of the strategy works further."""
            for strategy in logical_strategy:
                for r, c in number_cells:
                    update = strategy(r, c, board)
                    if update:
                        print(strategy.__name__, r, c)
                        return True
            return False

        while step():
            time.sleep(1)
            live.update(draw_board(board))
            pass
