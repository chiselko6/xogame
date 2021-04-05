from sqlalchemy import create_engine
from typing import Optional, List
import sqlalchemy as sa
from settings import Config
from contextlib import contextmanager
from uuid import UUID
from .models import Player, User, Game


class DBClient:

    def __init__(self) -> None:
        self._config = Config()
        self._engine = None

    def init(self) -> None:
        self._engine = create_engine(
            f"{self._config.db_dialect}://{self._config.db_user}:"
            f"{self._config.db_password}@{self._config.db_host}:"
            f"{self._config.db_port}/{self._config.db_name}"
        )

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

    def create_game(self, game: Game) -> None:
        query = sa.insert(Game).values(
            uuid=str(game.uuid),
            player_created=str(game.player_created),
            date_created=game.date_created,
        )

        with self.connect() as connection:
            connection.execute(query)

    def get_game(self, game_uuid: UUID) -> Optional[Game]:
        query = sa.select(Game).where(Game.uuid == str(game_uuid))

        with self.connect() as connection:
            return connection.execute(query).fetchone()

    def set_opponent(self, game_uuid: UUID, opponent: UUID) -> None:
        query = sa.update(Game).where(Game.uuid == str(game_uuid)).values(
            player_opponent=opponent,
        )

        with self.connect() as connection:
            connection.execute(query)

    def get_awaiting_games(self) -> List[Game]:
        query = sa.select(Game).where(Game.player_opponent.is_(None)).limit(10)

        with self.connect() as connection:
            return connection.execute(query).fetchmany()

    @contextmanager
    def connect(self):
        with self._engine.connect() as connection:
            yield connection

    @contextmanager
    def transaction(self):
        with self._engine.begin() as transaction:
            yield transaction
