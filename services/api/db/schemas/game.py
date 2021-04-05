from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class Game(BaseModel):
    uuid: UUID
    date_created: datetime
    player_created: UUID

    class Config:
        orm_mode = True
