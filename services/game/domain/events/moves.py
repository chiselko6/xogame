from pydantic import BaseModel
from uuid import UUID
from .base import BaseEvent

from ..state import Cell


class MoveEventParams(BaseModel):
    player: UUID
    cell: Cell


class MoveEvent(BaseEvent):
    name = "move"

    params: MoveEventParams
