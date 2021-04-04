from .base import BaseEvent
from uuid import UUID
from pydantic import BaseModel


class GameInitEventParams(BaseModel):
    grid_width: int
    grid_height: int
    initiator: UUID
    opponent: UUID
    winning_line_length: int


class GameInitEvent(BaseEvent):
    name = "game_init"

    params: GameInitEventParams
