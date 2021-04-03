from jose import jwt, exceptions
from settings import Config
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class TokenData(BaseModel):
    player_uuid: UUID
    game_uuid: UUID
    exp: datetime


def decode_token(token: str) -> TokenData:
    config = Config()

    try:
        decoded = jwt.decode(token, config.jwt_token_secret_key, algorithms=config.jwt_token_algorithm)
    except exceptions.JOSEError:
        raise ValueError("Invalid token")

    data = TokenData(**decoded)

    if datetime.now() > data["exp"]:
        raise ValueError("Token expired")

    return data
