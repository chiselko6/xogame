from typing import Sequence
from schemas.msg import WSResponse, BroadcastMessage
from schemas.auth import decode_token
from collections import defaultdict
from typing import Optional, MutableMapping, MutableSet
from uuid import UUID, uuid4
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from clients.game_service import Client as GameServiceClient
from clients.exceptions import ClientResponseError


app = FastAPI()
game_service = GameServiceClient()


async def reply(ws: WebSocket, msg: WSResponse) -> None:
    await ws.send_json(msg.json())


class Connections:

    def __init__(self):
        self._game_to_connections: MutableMapping[UUID, MutableSet[UUID]] = defaultdict(set)
        self._connection_to_game: MutableMapping[UUID, UUID] = {}
        self._connections: MutableMapping[UUID, WebSocket] = {}

    def connect(self, game_uuid: UUID, connection: WebSocket) -> UUID:
        connection_uuid = uuid4()

        self._game_to_connections[game_uuid].add(connection_uuid)
        self._connection_to_game[connection_uuid] = game_uuid
        self._connections[connection_uuid] = connection

        return connection_uuid

    def disconnect(self, connection_uuid: UUID) -> None:
        game_uuid = self._connection_to_game[connection_uuid]

        self._game_to_connections[game_uuid].remove(connection_uuid)
        del self._connection_to_game[connection_uuid]
        del self._connections[connection_uuid]

    def get_connections(self, game_uuid: UUID) -> Sequence[WebSocket]:
        return [
            self._connections[connection_uuid]
            for connection_uuid in self._game_to_connections[game_uuid]
        ]


connections = Connections()


@app.websocket("/ws")
async def websocket_handler(ws: WebSocket) -> None:
    await ws.accept()

    game_uuid: Optional[UUID] = None
    connection_uuid: Optional[UUID] = None

    while True:
        try:
            msg = await ws.receive_json()
        except WebSocketDisconnect:
            break

        if msg["type"] == "authorize":
            try:
                token_data = decode_token(msg["data"]["token"])
            except ValueError as e:
                await reply(ws, WSResponse(ok=False, error=str(e)))
                await ws.close()
                break
            else:
                game_uuid = token_data.game_uuid
                connection_uuid = connections.connect(game_uuid, ws)

        elif msg["type"] == "close":
            await ws.close()
            break
        elif msg["type"] == "echo":
            await reply(ws, WSResponse(ok=True, error=None))
        elif msg["type"] == "command":
            if UUID(msg["data"]["command"]["game_uuid"]) != game_uuid:
                await reply(ws, WSResponse(ok=False, error="Bad game reference"))
            else:
                try:
                    await game_service.send_command(msg["data"]["command"])
                except ClientResponseError:
                    await reply(ws, WSResponse(ok=False, error="Error applying the command"))
        else:
            await reply(ws, WSResponse(ok=False, error="Unknown message"))

    if connection_uuid is not None:
        connections.disconnect(connection_uuid)

    print("Websocket disconnected")


@app.post("/broadcast")
async def publish_msg(message: BroadcastMessage):
    for connection in connections.get_connections(message.game_uuid):
        await connection.send_json(message.payload)
