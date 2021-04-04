from pydantic import BaseSettings


class Config(BaseSettings):
    jwt_token_secret_key: str
    jwt_token_algorithm: str
    game_service_host: str
