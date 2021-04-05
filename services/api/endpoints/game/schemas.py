from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel


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
