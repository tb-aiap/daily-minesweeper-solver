"""Unit test for parser module."""

from pathlib import Path

import pytest

from daily_minesweeper import parser

EASY_5_MAP = "./src/tests/data/minesweeper-5x5-easy.html"
HARD_5_MAP = "./src/tests/data/minesweeper-5x5-hard.html"


@pytest.fixture
def easy_5_html():
    """Html for 5x5 easy."""
    with Path(EASY_5_MAP).open("r", encoding="utf-8") as f:
        html = f.read()

    return html


@pytest.fixture
def hard_5_html():
    """Html for 5x5 hard."""
    with Path(HARD_5_MAP).open("r", encoding="utf-8") as f:
        html = f.read()

    return html


def test_parse_easy_html_into_array(easy_5_html):
    """Test parsing easy 5x5 map."""
    result = parser.parse_html_into_array(easy_5_html)
    expected = [
        ["2", "", "", "", ""],
        ["2", "", "", "1", ""],
        ["", "2", "1", "1", ""],
        ["", "", "1", "", "1"],
        ["", "1", "", "", ""],
    ]
    assert result == expected


def test_parse_hard_html_into_array(hard_5_html):
    """Test parsing easy 5x5 map."""
    result = parser.parse_html_into_array(hard_5_html)
    expected = [
        ["2", "", "", "", "1"],
        ["", "", "3", "2", ""],
        ["2", "", "3", "", ""],
        ["2", "", "2", "3", ""],
        ["", "", "", "", ""],
    ]
    assert result == expected
