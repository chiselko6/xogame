from collections import namedtuple
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Sequence, Tuple
from uuid import UUID

from pydantic import BaseModel, validator

MIN_GRID_WIDTH = 3
MIN_GRID_HEIGHT = 3
MAX_GRID_WIDTH = 10
MAX_GRID_HEIGHT = 10

MIN_WINNING_LINE = 3


@dataclass
class Player:
    uuid: UUID


Cell = namedtuple("Cell", ["x", "y"])


class CellValue(Enum):
    EMPTY = "empty"
    X = "X"
    O = "O"


class Grid(BaseModel):
    cells: Dict[Cell, CellValue]
    width: int
    height: int

    @validator("cells")
    def validate_cells(
        cls, cells: Dict[Cell, CellValue], values: Dict[str, Any]
    ) -> Dict[Cell, CellValue]:
        width = values["width"]
        height = values["height"]

        for cell in cells:
            if not (0 <= cell.x < width) or not (0 <= cell.y < height):
                raise ValueError("Cell position is out of range")

        return cells

    def set_value(self, cell: Cell, value: CellValue) -> None:
        self.cells[cell] = value

    def get_value(self, cell: Cell) -> CellValue:
        return self.cells[cell]

    def get_winning_line(self, winning_line_length: int) -> Optional[Sequence[Cell]]:
        assert winning_line_length >= MIN_WINNING_LINE

        for x in range(self.width):
            for y in range(self.height):
                for shift_x, shift_y in [
                    (0, 1),
                    (1, 0),
                    (1, -1),
                    (1, 1),
                ]:
                    cells_to_check = [
                        Cell(x + shift_x * d, y + shift_y * d)
                        for d in range(winning_line_length)
                    ]

                    if all(
                        [
                            0 <= cell.x < self.width and 0 <= cell.y < self.height
                            for cell in cells_to_check
                        ]
                    ):
                        cell_values = [
                            self.cells[cell].value for cell in cells_to_check
                        ]

                        if cell_values.count(cell_values[0]) == len(cell_values):
                            return cells_to_check
        return None


class State:
    def __init__(self, grid_size: Tuple[int, int], winning_line: int) -> None:
        self._players: List[UUID] = []
        self._player_to_start: Optional[UUID] = None
        self._player_to_move: Optional[UUID] = None
        self._finished = False
        self._winner: Optional[UUID] = None

        width, height = grid_size
        assert MIN_GRID_WIDTH <= width <= MAX_GRID_WIDTH
        assert MIN_GRID_HEIGHT <= height <= MAX_GRID_HEIGHT
        assert MIN_WINNING_LINE <= winning_line < max(grid_size)

        self._grid = Grid(
            width=width,
            height=height,
            cells={
                Cell(x=x, y=y): CellValue.EMPTY
                for x in range(width)
                for y in range(height)
            },
        )
        self._winning_line = winning_line

    @property
    def winner(self) -> Optional[UUID]:
        return self._winner

    @property
    def finished(self) -> bool:
        return self._finished

    @property
    def winning_line(self) -> Optional[Sequence[Cell]]:
        return self._grid.get_winning_line(self._winning_line)

    def _check_win(self) -> bool:
        winning_line = self._grid.get_winning_line(self._winning_line)
        if winning_line is not None:
            self._finished = True

            winning_value = self._grid.get_value(winning_line[0])
            if winning_value == self.get_player_value(self._players[0]):
                self._winner = self._players[0]
            else:
                self._winner = self._players[1]

            return True
        return False

    def get_player_value(self, player_uuid: UUID) -> CellValue:
        if player_uuid not in self._players:
            # TODO
            raise ValueError()

        return CellValue.X if player_uuid == self._player_to_start else CellValue.O

    def set_players(self, players: Sequence[UUID]) -> None:
        if len(players) != 2:
            # TODO
            raise ValueError()

        self._players = players

    def set_player_to_start(self, player_to_start: UUID) -> None:
        if player_to_start not in self._players:
            # TODO
            raise ValueError()

        self._player_to_start = player_to_start

    def move(self, player_uuid: UUID, cell: Cell) -> None:
        if self.finished:
            # TODO
            raise ValueError()

        if self._player_to_move != player_uuid:
            # TODO
            raise ValueError()

        self._grid.set_value(cell, self.get_player_value(player_uuid))

        if self._player_to_move == self._players[0]:
            self._player_to_move = self._players[1]
        else:
            self._player_to_move = self._players[0]

        self._check_win()
