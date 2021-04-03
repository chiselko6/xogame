from sqlalchemy import create_engine
from typing import Optional
import sqlalchemy as sa
from settings import DB_DIALECT, DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER
from contextlib import contextmanager
from uuid import UUID
from .models import Player, User


class DBClient:

    def __init__(self) -> None:
        self._engine = None

    def init(self) -> None:
        self._engine = create_engine(f"{DB_DIALECT}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

    def insert_player(self, player: Player) -> None:
        query = sa.insert(Player).values(
            uuid=str(player.uuid),
            date_joined=player.date_joined,
            username=player.username,
        )

        with self.connect() as connection:
            connection.execute(query)

    def get_player_by_uuid(self, player_uuid: UUID) -> Optional[Player]:
        query = sa.select(Player).where(Player.uuid == str(player_uuid))

        with self.connect() as connection:
            return connection.execute(query).fetchone()

    def get_player_by_username(self, username: str) -> Optional[Player]:
        query = sa.select(Player).where(Player.username == username)

        with self.connect() as connection:
            return connection.execute(query).fetchone()

    def get_user(self, username: str) -> Optional[User]:
        query = sa.select(User).where(User.username == username)

        with self.connect() as connection:
            return connection.execute(query).fetchone()

    @contextmanager
    def connect(self):
        with self._engine.connect() as connection:
            yield connection

    @contextmanager
    def transaction(self):
        with self._engine.begin() as transaction:
            yield transaction
