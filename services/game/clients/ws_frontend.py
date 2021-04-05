import json
from urllib.parse import urljoin

from aiohttp import ClientResponseError as HTTPError
from aiohttp import ClientSession

from domain.events.base import BaseEvent
from settings import Config

from .exceptions import ClientResponseError


class Client:
    def __init__(self) -> None:
        config = Config()

        self._host = config.ws_frontend_host

    async def broadcast(self, event: BaseEvent) -> None:
        async with ClientSession() as session:
            async with session.post(
                urljoin(self._host, "/broadcast"), json=json.loads(event.json())
            ) as resp:
                try:
                    resp.raise_for_status()
                except HTTPError:
                    raise ClientResponseError()
