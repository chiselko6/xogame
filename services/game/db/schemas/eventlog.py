from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class BaseEvent(BaseModel):
    game_uuid: UUID
    name: str
    sequence: int
    timestamp: datetime
    player_uuid: UUID
    params: BaseModel

    class Config:
        orm_mode = True
