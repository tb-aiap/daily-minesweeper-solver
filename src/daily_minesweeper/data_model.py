"""Module to define board and cells."""

from dataclasses import dataclass
from enum import StrEnum


class CellState(StrEnum):
    """Container for different states in a cell."""

    unmarked = "?"
    suspect = "S"
    flag = "F"
    empty = "O"
    is_number = "n"


@dataclass
class Cell:
    """Dataclass for a single cell within the board."""

    state: CellState
    value: int

    x: int
    y: int
