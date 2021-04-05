from collections import namedtuple
from datetime import datetime
from typing import ClassVar
from uuid import UUID

from pydantic import BaseModel

from ..events.base import BaseEvent
from ..events.game import GameInitEvent, GameInitEventParams
from ..events.moves import MoveEvent, MoveEventParams


class BaseCommand(BaseModel):
    name: ClassVar
    game_uuid: UUID
    sequence: int
    player_uuid: UUID
    timestamp: datetime
    params: BaseModel


class GameInitCommandParams(BaseModel):
    grid_width: int
    grid_height: int
    initiator: UUID
    opponent: UUID
    winning_line_length: int


class GameInitCommand(BaseCommand):
    name = "game_init"
    params: GameInitCommandParams


Cell = namedtuple("Cell", ["x", "y"])


class MoveCommandParams(BaseModel):
    player: UUID
    cell: Cell


class MoveCommand(BaseCommand):
    name = "move"
    params: MoveCommandParams


def apply_command(command: BaseCommand) -> BaseEvent:
    if isinstance(command, GameInitCommand):
        return GameInitEvent(
            game_uuid=command.game_uuid,
            sequence=command.sequence,
            player_uuid=command.player_uuid,
            timestamp=command.timestamp,
            params=GameInitEventParams(**command.params.dict()),
        )
    elif isinstance(command, MoveCommand):
        return MoveEvent(
            game_uuid=command.game_uuid,
            sequence=command.sequence,
            player_uuid=command.player_uuid,
            timestamp=command.timestamp,
            params=MoveEventParams(**command.params.dict()),
        )

    raise ValueError("Unknown command")
