import json
from typing import Any, Mapping
from urllib.parse import urljoin

from aiohttp import ClientResponseError as HTTPError
from aiohttp import ClientSession

from settings import Config

from .exceptions import ClientResponseError


class Client:
    def __init__(self) -> None:
        config = Config()

        self._host = config.game_service_host

    async def send_command(self, body: Mapping[str, Any]) -> None:
        """Send the command to game service"""

        async with ClientSession() as session:
            async with session.post(
                urljoin(self._host, "/game/apply"), json=json.loads(json.dumps(body))
            ) as resp:
                try:
                    resp.raise_for_status()
                except HTTPError:
                    raise ClientResponseError()
