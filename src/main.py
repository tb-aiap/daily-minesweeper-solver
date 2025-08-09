"""Main entry for solving minesweeper."""

import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from daily_minesweeper import constants, parser, solver
from daily_minesweeper.data_model import CellState

logical_strategy = [
    solver.flag_all_numbers,
    solver.flag_remaining_unmarked,
]


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
    driver.get(constants.BASE_URL + constants.EASY_20 + "/")

    bs = BeautifulSoup(driver.page_source, "html.parser")
    result = bs.find(id=constants.GAME_ID)

    ## LOAD THE HTML INTO 2D ARRAY
    array_board = parser.parse_html_into_array(str(result))

    ## INITIALIZE THE BOARD
    board = solver.Board(array_board)
    clickable = [
        (r, c)
        for r in range(board.rows)
        for c in range(board.columns)
        if board[r][c].state == CellState.unmarked
    ]

    ## SOLVE THE BOARD
    solver.solve_logically(board, logical_strategy)

    ## RECORD THE COORDINATE POSITION
    flags = [
        (r, c)
        for r in range(board.rows)
        for c in range(board.columns)
        if board[r][c].state == CellState.flag
    ]

    puzzle = driver.find_elements(By.CLASS_NAME, "cell-off")
    actions = ActionChains(driver)

    if len(clickable) != len(puzzle):
        raise Exception(f"expect clickable cells to be similar.{clickable=}=={puzzle=}")

    for p, c in zip(puzzle, clickable):
        if c in flags:
            print(p)
            actions.context_click(p).perform()


if __name__ == "__main__":
    main()
