"""Module to get and parse minesweeper data."""

import re
from bs4 import BeautifulSoup


def parse_html_into_array(html_str: str) -> list[list[str]]:
    """Parse minesweeper html into 2d array.

    Args:
        html_str (str): html retrieve from website

    Returns:
        list[list[int]]: 2d array list of list with numbers or "".
    """
    bs = BeautifulSoup(html_str, "html.parser")
    result = bs.find_all(class_="cell")

    idx = 3
    full_arr = []
    arr = []
    for r in result:
        top_px_level = int(re.search(r"top:\s*(\d+)\s*px;", r["style"]).group(1))
        number = r.find(class_="number").text
        if idx == top_px_level:
            arr.append(number)
        elif idx < int(top_px_level):
            idx = int(top_px_level)
            row_arr = arr.copy()
            full_arr.append(row_arr)
            arr = [number]
    else:
        row_arr = arr.copy()
        full_arr.append(row_arr)

    return full_arr


if __name__ == "__main__":
    ...
