import json
from datetime import datetime
from urllib.parse import urljoin
from uuid import UUID

from aiohttp import ClientResponseError as HTTPError
from aiohttp import ClientSession

from settings import Config

from .exceptions import ClientResponseError


class Client:
    def __init__(self) -> None:
        config = Config()

        self._host = config.game_service_host

    async def start_game(
        self,
        game_uuid: UUID,
        *,
        grid_size: int,
        winning_line_length: int,
        initiator: UUID,
        opponent: UUID
    ) -> None:
        """Send a command to the game service to start the game"""

        params = {
            "grid_width": grid_size,
            "grid_height": grid_size,
            "initiator": str(initiator),
            "opponent": str(opponent),
            "winning_line_length": winning_line_length,
        }
        payload = {
            "name": "game_init",
            "sequence": 1,
            "game_uuid": str(game_uuid),
            "player_uuid": str(initiator),
            "timestamp": str(datetime.utcnow()),
            "params": params,
        }
        async with ClientSession() as session:
            async with session.post(
                urljoin(self._host, "/game/apply"), json=json.loads(json.dumps(payload))
            ) as resp:
                try:
                    resp.raise_for_status()
                except HTTPError:
                    raise ClientResponseError()
