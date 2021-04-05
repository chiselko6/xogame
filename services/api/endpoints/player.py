from uuid import UUID

from fastapi import FastAPI, HTTPException

from db.client import DBClient
from db.schemas.player import Player as PlayerSchema

app = FastAPI()

db_client = DBClient()
db_client.init()


@app.get("/{player_uuid}", response_model=PlayerSchema)
async def get_player(player_uuid: UUID):
    player = db_client.get_player_by_uuid(player_uuid)

    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return player
