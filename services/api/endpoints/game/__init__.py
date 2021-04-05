from datetime import datetime
from uuid import uuid4

from fastapi import Depends, FastAPI

from clients.game_service import Client
from db.client import DBClient
from db.schemas.game import Game as GameSchema

from ..auth import oauth2_scheme
from ..auth.util import decode_auth_token
from .schemas import (AwaitingGame, AwaitingGamesResponse, ConnectGameRequest,
                      GameCreateRequest, GameCreateResponse)

app = FastAPI()

db_client = DBClient()
db_client.init()

game_service_client = Client()


@app.post("/", response_model=GameCreateResponse)
async def create_game(game: GameCreateRequest, token: str = Depends(oauth2_scheme)):
    decoded = decode_auth_token(token)

    player = db_client.get_player_by_username(decoded.username)
    new_game = GameSchema(
        uuid=uuid4(), date_created=datetime.utcnow(), player_created=player.uuid
    )
    db_client.create_game(new_game)

    return GameCreateResponse(game_uuid=new_game.uuid)


@app.get("/awaiting", response_model=AwaitingGamesResponse)
async def get_awaiting_games(token: str = Depends(oauth2_scheme)):
    return AwaitingGamesResponse(
        games=[
            AwaitingGame(
                uuid=game.uuid,
                player_created=game.player_created,
                date_created=game.date_created,
            )
            for game in db_client.get_awaiting_games()
        ]
    )


@app.post("/connect")
async def connect(game: ConnectGameRequest, token: str = Depends(oauth2_scheme)):
    decoded = decode_auth_token(token)

    player = db_client.get_player_by_username(decoded.username)

    db_game = db_client.get_game(game.uuid)
    db_client.set_opponent(game.uuid, player.uuid)

    # currently hardcoded params, but should be stored and retrieved
    await game_service_client.start_game(
        grid_size=6,
        winning_line_length=4,
        initiator=db_game.player_created,
        opponent=player.uuid,
    )
