"""Main entry for solving minesweeper."""

import time
from typing import Callable

from bs4 import BeautifulSoup
from rich.console import Console
from rich.live import Live
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from daily_minesweeper import constants, display, parser, solver
from daily_minesweeper.data_model import CellState

URL = constants.BASE_URL + constants.EASY_20 + "/"

console = Console()

logical_strategy = [
    solver.flag_all_numbers,
    solver.flag_remaining_unmarked,
]


def solve(
    board: solver.Board, strategies: list[Callable[[int, int, solver.Board], bool],]
) -> None:
    """Loop through each solving strategy on the board and try to clear as much as possible."""
    number_cells = board.get_all_cells_by_state(CellState.is_number)

    def step() -> bool:
        """Continuously loop all strategies to apply. Stops when none of the strategy works further."""
        return any(
            strategy(r, c, board) for strategy in strategies for r, c in number_cells
        )

    # render the board after each pass of all strategies.
    with Live(display.draw_board(board), console=console, refresh_per_second=4) as live:
        while step():
            time.sleep(0.1)
            live.update(display.draw_board(board))
            pass


def main() -> None:
    """Main function for solving.

    1. Opens up the minesweeper website of selected difficulty.
    2. Wait for the html to load properly.
    3. Parse the html into 2D array.
    4. Apply the series of functions as strategy to solve the board.
    5. Translate the flagged cell into positions to click for website.
    """
    ## OPEN THE WEB BROWSER
    driver = webdriver.Firefox()
    driver.get(URL)

    bs = BeautifulSoup(driver.page_source, "html.parser")
    result = bs.find(id=constants.GAME_ID)

    ## LOAD THE HTML INTO 2D ARRAY
    array_board = parser.parse_html_into_array(str(result))

    ## INITIALIZE THE BOARD
    board = solver.Board(array_board)
    clickable = board.get_all_cells_by_state(CellState.unmarked)

    ## SOLVE THE BOARD WITH DISPLAY
    solve(board, logical_strategy)

    ## RECORD THE COORDINATE POSITION
    flags = board.get_all_cells_by_state(CellState.flag)

    ## UPDATE THE WEBPAGE
    web_clickable = driver.find_elements(By.CLASS_NAME, "cell-off")

    if len(clickable) != len(web_clickable):
        raise Exception(
            f"expect clickable cells not same len.{len(clickable)=}=={len(web_clickable)=}"
        )

    for p, c in zip(web_clickable, clickable):
        if c in flags:
            actions = ActionChains(driver, duration=250)
            actions.context_click(p).perform()


if __name__ == "__main__":
    main()
