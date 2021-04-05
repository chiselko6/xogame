from typing import Any
from urllib.parse import urljoin

from aiohttp import ClientResponseError as HTTPError
from aiohttp import ClientSession

from settings import Config

from .exceptions import ClientResponseError


class Client:
    def __init__(self) -> None:
        config = Config()

        self._host = config.game_service_host

    async def send_command(self, body: Any) -> None:
        async with ClientSession() as session:
            async with session.post(
                urljoin(self._host, "/game/apply"), data=body
            ) as resp:
                try:
                    resp.raise_for_status()
                except HTTPError:
                    raise ClientResponseError()
