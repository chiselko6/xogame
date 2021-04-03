from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class Player(BaseModel):
    uuid: UUID
    date_joined: datetime
    username: str

    class Config:
        orm_mode = True
