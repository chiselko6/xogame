from db.schemas.eventlog import BaseEvent as DBEvent

from .events.base import BaseEvent
from .events.game import GameInitEvent, GameInitEventParams
from .events.moves import MoveEvent, MoveEventParams


def load_event(event: DBEvent) -> BaseEvent:
    game_event_params = [
        (GameInitEvent, GameInitEventParams),
        (MoveEvent, MoveEventParams),
    ]

    for event_param in game_event_params:
        if event_param[0].name == event.name:
            return event_param[0](
                **event.dict(), params=event_param[1](**event.params.dict())
            )

    raise ValueError("Unknown event")
