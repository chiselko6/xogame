from fastapi import FastAPI
from endpoints.player import app as player_app
from endpoints.auth import app as auth_app
from endpoints.game import app as game_app

app = FastAPI()


@app.get("/healthcheck")
async def healthcheck():
    return "OK"


app.mount("/players", player_app)
app.mount("/game", game_app)
app.mount("/auth", auth_app)
