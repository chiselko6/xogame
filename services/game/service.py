from fastapi import FastAPI
from endpoints.events import app as game_app

app = FastAPI()


@app.get("/healthcheck")
async def healthcheck():
    return "OK"


app.mount("/game", game_app)
