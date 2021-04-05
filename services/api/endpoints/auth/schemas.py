from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class TokenType(Enum):
    BEARER = "Bearer"
    INTRA = "Intra"


class Token(BaseModel):
    access_token: str
    token_type: TokenType


class AuthTokenData(BaseModel):
    username: str


class IntraTokenData(BaseModel):
    player_uuid: UUID
    game_uuid: UUID
