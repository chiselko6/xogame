import json
from contextlib import contextmanager
from typing import Any, Dict, Sequence
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy import create_engine

from domain.events.base import BaseEvent
from domain.events.game import GameInitEvent, GameInitEventParams
from domain.events.moves import MoveEvent, MoveEventParams
from settings import Config

from .models import Eventlog


def load_event(event: Dict[str, Any], params: Dict[str, Any]) -> BaseEvent:
    game_event_params = [
        (GameInitEvent, GameInitEventParams),
        (MoveEvent, MoveEventParams),
    ]

    for event_param in game_event_params:
        if event_param[0].name == event["name"]:
            return event_param[0](**event, params=event_param[1](**params))

    raise ValueError("Unknown event")


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
            query = (
                sa.select(Eventlog)
                .where(Eventlog.game_uuid == str(game_uuid))
                .order_by(Eventlog.sequence)
            )

            db_events = connection.execute(query).fetchmany()

            events = []
            for db_event in db_events:
                event_dict = dict(db_event._mapping)
                params = json.loads(event_dict.pop("params"))
                events.append(load_event(event_dict, params))
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
