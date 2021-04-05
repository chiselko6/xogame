from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Player(BaseModel):
    uuid: UUID
    date_joined: datetime
    username: str

    class Config:
        orm_mode = True
