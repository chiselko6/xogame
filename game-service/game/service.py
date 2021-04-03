from fastapi import FastAPI
from endpoints.events import app as events_app

app = FastAPI()


@app.get("/healthcheck")
async def healthcheck():
    return "OK"


app.mount("/events", events_app)
