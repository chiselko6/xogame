from pydantic import BaseSettings


class Config(BaseSettings):
    db_dialect: str
    db_user: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str
