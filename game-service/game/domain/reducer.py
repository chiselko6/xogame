from operator import methodcaller
from typing import Optional, Sequence
from random import choice

from .events.base import BaseEvent
from .events.game import GameInitEventParams
from .events.moves import MoveEventParams
from .state import State


class Reducer:

    def __init__(self) -> None:
        self._state: Optional[State] = None

    @property
    def state(self) -> Optional[State]:
        return self._state

    def apply_event(self, event: BaseEvent) -> None:
        methodcaller(f"apply__{event.name}", self, event.params)

    def apply_events(self, events: Sequence[BaseEvent]) -> None:
        for event in events:
            methodcaller(f"apply__{event.name}", self, event.params)

    def apply__move(self, params: MoveEventParams) -> None:
        self._state.move(params.player, params.cell)

    def apply__game_init(self, params: GameInitEventParams) -> None:
        self._state = State(grid_size=(params.grid_width, params.grid_height), winning_line=params.winning_line_length)

        players = [params.initiator, params.opponent]
        self._state.set_players(players)
        self._state.set_player_to_start(choice(players))
