from datetime import datetime
from typing import Any, Dict, List
from uuid import UUID

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from clients.ws_frontend import Client
from db.client import DBClient
from domain.commands import (BaseCommand, GameInitCommand,
                             GameInitCommandParams, MoveCommand,
                             MoveCommandParams, apply_command)
from domain.events.base import BaseEvent
from domain.reducer import Reducer

app = FastAPI()

db_client = DBClient()
db_client.init()

ws_client = Client()


class CommandSchema(BaseModel):
    game_uuid: UUID
    name: str
    sequence: int
    player_uuid: UUID
    timestamp: datetime
    params: Dict[str, Any]


def load_command(command: CommandSchema) -> BaseCommand:
    available_commands = [
        (GameInitCommand, GameInitCommandParams),
        (MoveCommand, MoveCommandParams),
    ]

    for available_command in available_commands:
        if available_command[0].name == command.name:
            cmd_dict = command.dict()
            params = cmd_dict.pop("params")
            return available_command[0](
                **cmd_dict, params=available_command[1](**params)
            )

    raise ValueError("Unknown command")


@app.post("/apply")
async def handle_event(command: CommandSchema):
    game_uuid = command.game_uuid
    command_event = apply_command(load_command(command))

    game_events = db_client.get_game_events(game_uuid)

    # verify the event is applicable
    reducer = Reducer()
    reducer.apply_events(game_events)
    reducer.apply_event(command_event)

    # save the event
    db_client.insert_events([command_event])

    await ws_client.broadcast(command_event)


@app.get("/fetch/{game_uuid}", response_model=List[BaseEvent])
async def fetch_events(game_uuid: UUID):
    events = db_client.get_game_events(game_uuid)

    if not events:
        raise HTTPException(status_code=404, detail="Game not found")

    return events
