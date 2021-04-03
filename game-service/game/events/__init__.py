from db.schemas.eventlog import BaseEvent as DBEvent
from .game import GameInitEvent, GameInitEventParams
from .moves import MoveEvent, MoveEventParams
from .base import BaseEvent

__all__ = [
    'BaseEvent',
    'GameInitEvent',
    'GameInitEventParams',
    'MoveEvent',
    'MoveEventParams',
    'load_event',
]


def load_event(event: DBEvent) -> BaseEvent:
    game_event_params = [
        (GameInitEvent, GameInitEventParams),
        (MoveEvent, MoveEventParams),
    ]

    for event_param in game_event_params:
        if event_param[0].name == event.name:
            return event_param[0](**event.dict(), params=event_param[1](**event.params.dict()))

    raise ValueError("Unknown event")
