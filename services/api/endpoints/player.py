from fastapi import FastAPI, HTTPException

from db.schemas.player import Player as PlayerSchema
from db.client import DBClient
from uuid import UUID

app = FastAPI()

db_client = DBClient()
db_client.init()


@app.post("/", response_model=PlayerSchema)
async def create_player(player: PlayerSchema):
    db_client.insert_player(player)

    return player


@app.get("/{player_uuid}", response_model=PlayerSchema)
async def read_user(player_uuid: UUID):
    player = db_client.get_player_by_uuid(player_uuid)

    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return player