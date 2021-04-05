from fastapi import Depends, FastAPI, HTTPException

from db.client import DBClient

from ..auth import oauth2_scheme
from ..auth.util import decode_auth_token
from .schemas import PlayerGetMeResponse

app = FastAPI()

db_client = DBClient()
db_client.init()


@app.get("/me", response_model=PlayerGetMeResponse)
async def get_me(token: str = Depends(oauth2_scheme)):
    """Fetch current player info"""

    auth_token = decode_auth_token(token)
    player = db_client.get_player_by_username(auth_token.username)

    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return PlayerGetMeResponse(uuid=player.uuid)
