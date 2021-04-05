from aiohttp import ClientSession, ClientResponseError as HTTPError
from settings import Config
from urllib.parse import urljoin
from .exceptions import ClientResponseError
from uuid import UUID
from datetime import datetime


class Client:

    def __init__(self) -> None:
        config = Config()

        self._host = config.game_service_host

    async def start_game(self, *, grid_size: int, winning_line_length: int, initiator: UUID, opponent: UUID) -> None:
        params = {
            "grid_width": grid_size,
            "grid_height": grid_size,
            "initiator": initiator,
            "opponent": opponent,
            "winning_line_length": winning_line_length,
        }
        payload = {
            "name": "game_init",
            "sequence": 1,
            "player_uuid": initiator,
            "timestamp": datetime.utcnow(),
            "params": params,
        }
        async with ClientSession() as session:
            async with session.post(urljoin(self._host, "/game/apply"), data=payload) as resp:
                try:
                    resp.raise_for_status()
                except HTTPError:
                    raise ClientResponseError()
