"""Main entry for solving minesweeper."""

import sys
import time
from typing import Callable

from bs4 import BeautifulSoup
from rich.console import Console
from rich.live import Live
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from daily_minesweeper import constants, display, parser, solver, utils
from daily_minesweeper.data_model import CellState

DIFFICULTY = utils.parse_sysargv_difficulty(sys.argv)

WEBPAGE_CLICK_SPEED = 100  # in milliseconds
CONSOLE_CLICK_SPEED = 10  # in milliseconds
SCROLL_WAIT_TIME = 100  # in milliseconds

console = Console()

## Main strategies for solving the puzzle, in order.
logical_strategy = [
    solver.flag_all_numbers,
    solver.flag_remaining_unmarked,
    solver.deduce_from_neighbors_and_flag,
    solver.suspect_adjacent_candidates_and_mark_neighbor_empty,
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
            time.sleep(CONSOLE_CLICK_SPEED / 1000)
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
    console.print(f"[bold blue]💣 Solving for difficulty {DIFFICULTY} 💣[/]")
    ## OPEN THE WEB BROWSER
    driver = webdriver.Firefox()
    driver.get(constants.BASE_URL + DIFFICULTY + "/")
    driver.find_element(By.ID, "SideClose").click()

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

    vh = driver.get_window_size()["height"] - 100
    for p, c in zip(web_clickable, clickable):
        if c in flags:
            scroll_position = driver.execute_script("return window.pageYOffset;")
            scroll_y = max((p.location["y"] - (vh + scroll_position)), 0)
            if scroll_y:
                scroll_action = ActionChains(driver, duration=100)
                scroll_action.scroll_by_amount(delta_x=0, delta_y=scroll_y).perform()
                time.sleep(SCROLL_WAIT_TIME / 1000)

            actions = ActionChains(driver, duration=WEBPAGE_CLICK_SPEED)
            actions.context_click(p).perform()


if __name__ == "__main__":
    main()
