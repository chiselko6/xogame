from sqlalchemy import create_engine
from typing import Sequence
import sqlalchemy as sa
from settings import Config
from contextlib import contextmanager
from uuid import UUID
from .models import Eventlog
from .schemas.eventlog import BaseEvent as DBEvent
from domain import BaseEvent, load_event
import json


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

    def get_game_events(self, game_uuid: UUID) -> Sequence[BaseEvent]:
        with self.connect() as connection:
            query = sa.select(Eventlog).where(Eventlog.game_uuid == str(game_uuid)).order_by(Eventlog.sequence)

            db_events = connection.execute(query).fetchmany()

            events = []
            for db_event in db_events:
                event_dict = dict(db_event._mapping)
                params = json.loads(event_dict.pop('params'))
                events.append(
                    load_event(DBEvent(**event_dict, params=params))
                )
            return events

    def insert_events(self, events: Sequence[BaseEvent]) -> None:
        with self.transaction() as transaction:
            for event in events:
                query = sa.insert(Eventlog).values(
                    game_uuid=str(event.game_uuid),
                    name=event.name,
                    sequence=event.sequence,
                    player_uuid=str(event.player_uuid),
                    timestamp=event.timestamp,
                    params=event.params.json(),
                )

                transaction.execute(query)

    @contextmanager
    def connect(self):
        with self._engine.connect() as connection:
            yield connection

    @contextmanager
    def transaction(self):
        with self._engine.begin() as transaction:
            yield transaction
