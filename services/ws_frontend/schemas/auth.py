from jose import jwt
from settings import Config
from pydantic import BaseModel
from uuid import UUID


class TokenData(BaseModel):
    player_uuid: UUID
    game_uuid: UUID


def decode_token(token: str) -> TokenData:
    config = Config()

    return TokenData(**jwt.decode(token, config.jwt_token_secret_key, algorithms=config.jwt_token_algorithm))
