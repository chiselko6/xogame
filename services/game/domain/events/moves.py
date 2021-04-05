from uuid import UUID

from pydantic import BaseModel

from ..state import Cell
from .base import BaseEvent


class MoveEventParams(BaseModel):
    player: UUID
    cell: Cell


class MoveEvent(BaseEvent):
    name = "move"

    params: MoveEventParams
