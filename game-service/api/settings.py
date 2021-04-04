from pydantic import BaseSettings


class Config(BaseSettings):
    db_dialect: str
    db_user: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str

    jwt_token_secret_key: str
    jwt_token_algorithm: str
    jwt_token_access_expire_minutes: int
