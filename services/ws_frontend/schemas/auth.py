from uuid import UUID

from jose import jwt
from pydantic import BaseModel

from settings import Config


class TokenData(BaseModel):
    player_uuid: UUID
    game_uuid: UUID


def decode_token(token: str) -> TokenData:
    config = Config()

    return TokenData(
        **jwt.decode(
            token, config.jwt_token_secret_key, algorithms=config.jwt_token_algorithm
        )
    )
