from pydantic import BaseModel
from uuid import UUID
from typing import List
from datetime import datetime


class GameCreateRequest(BaseModel):
    size: int
    winning_line_length: int


class GameCreateResponse(BaseModel):
    game_uuid: UUID


class AwaitingGame(BaseModel):
    uuid: UUID
    player_created: UUID
    date_created: datetime


class AwaitingGamesResponse(BaseModel):
    games: List[AwaitingGame]


class ConnectGameRequest(BaseModel):
    uuid: UUID
