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
