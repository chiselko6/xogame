import json
from datetime import datetime, timedelta
from uuid import UUID

from jose import jwt

from db.client import DBClient
from settings import Config

from .schemas import AuthTokenData, IntraTokenData

db_client = DBClient()
db_client.init()

config = Config()


def encode_auth_token(username: str) -> str:
    auth_token_data = AuthTokenData(username=username)

    payload = {
        **auth_token_data.dict(),
        "exp": datetime.utcnow()
        + timedelta(minutes=config.jwt_auth_token_access_expire_minutes),
    }

    return jwt.encode(
        payload,
        config.jwt_auth_token_secret_key,
        algorithm=config.jwt_auth_token_algorithm,
    )


def decode_auth_token(token: str) -> AuthTokenData:
    return AuthTokenData(
        **jwt.decode(
            token,
            config.jwt_auth_token_secret_key,
            algorithms=config.jwt_auth_token_algorithm,
        )
    )


def encode_intra_token(username: str, game_uuid: UUID) -> str:
    user = db_client.get_player_by_username(username)

    intra_token_data = IntraTokenData(
        player_uuid=user.uuid,
        game_uuid=game_uuid,
    )

    payload = {
        **json.loads(intra_token_data.json()),
        "exp": datetime.utcnow()
        + timedelta(minutes=config.jwt_intra_token_access_expire_minutes),
    }

    return jwt.encode(
        payload,
        config.jwt_intra_token_secret_key,
        algorithm=config.jwt_intra_token_algorithm,
    )
