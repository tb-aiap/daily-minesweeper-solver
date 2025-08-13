"""Utilities module."""

from bs4 import BeautifulSoup
from selenium import webdriver

from . import constants as c


def get_sample_minesweeper_game(url_address: str = None) -> str:
    """Get retrieve sample minesweeper game for testing purpose.

    Args:
        url_address (str, optional): url with difficulty

    Returns:
        str: html page of the minesweeper
    """
    if url_address is None:
        url_address = c.BASE_URL + c.EASY_5

    driver = webdriver.Firefox()
    driver.get(url_address)

    bs = BeautifulSoup(driver.page_source, "html.parser")
    result = bs.find(id=c.GAME_ID)

    driver.quit()

    return str(result)


def parse_sysargv_difficulty(args: list[str]) -> str:
    """Get the difficulty from command line.

    Expects from a list of difficulty in constants.py, defaults to daily if none entered.

    Args:
        args (list[str]): from sys.argv

    Raises:
        Exception: if difficulty is not in expected list

    Returns:
        str: one of the constants predefined.
    """
    if len(args) == 1:
        return c.DAILY

    difficulty = args[1]
    if difficulty not in c.DIFFICULTY:
        raise Exception(
            f"expecting one of the following options {c.DIFFICULTY}",
            f"received {difficulty}",
        )

    return getattr(c, difficulty.upper())
