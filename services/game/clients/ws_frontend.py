from aiohttp import ClientSession, ClientResponseError as HTTPError
from settings import Config
from urllib.parse import urljoin
from .exceptions import ClientResponseError
from domain.events.base import BaseEvent


class Client:

    def __init__(self) -> None:
        config = Config()

        self._host = config.ws_frontend_host

    async def broadcast(self, event: BaseEvent) -> None:
        async with ClientSession() as session:
            async with session.post(urljoin(self._host, "/broadcast"), data=event.json()) as resp:
                try:
                    resp.raise_for_status()
                except HTTPError:
                    raise ClientResponseError()
