from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Game(BaseModel):
    uuid: UUID
    date_created: datetime
    player_created: UUID

    class Config:
        orm_mode = True
