"""Module to define board and cells."""

from dataclasses import dataclass
from enum import StrEnum


class CellState(StrEnum):
    """Container for different states in a cell."""

    unmarked = "unmarked"
    suspect = "suspect"
    flag = "flagged"
    empty = "empty"
    is_number = "is_number"


@dataclass
class Cell:
    """Dataclass for a single cell within the board."""

    state: CellState
    value: int
    x: int
    y: int
