from pydantic import BaseModel
from datetime import datetime
from typing import ClassVar
from uuid import UUID


class BaseEvent(BaseModel):
    name: ClassVar

    game_uuid: UUID
    sequence: int
    player_uuid: UUID
    timestamp: datetime
    params: BaseModel
