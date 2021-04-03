from fastapi import FastAPI, HTTPException
from typing import List
from events.base import BaseEvent
from db.client import DBClient
from uuid import UUID
from reducer import Reducer
from events import load_event
from events.commands import BaseCommand, GameInitCommand, GameInitCommandParams, MoveCommand, MoveCommandParams, apply_command
from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime

app = FastAPI()

db_client = DBClient()
db_client.init()


class CommandSchema(BaseModel):
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
            return available_command[0](**cmd_dict, params=available_command[1](**params))

    raise ValueError("Unknown command")


@app.post("/apply/{game_uuid}")
async def handle_event(game_uuid: UUID, command: CommandSchema):
    command_event = apply_command(load_command(command))

    game_events = [
        load_event(db_event)
        for db_event in db_client.fetch_game_events(game_uuid)
    ]

    # verify the event is applicable
    reducer = Reducer()
    reducer.apply_events(game_events)
    reducer.apply_event(command_event)

    # save the event
    db_client.insert_events(game_uuid, [command_event])


@app.get("/fetch/{game_uuid}", response_model=List[BaseEvent])
async def fetch_events(game_uuid: UUID):
    events = [
        load_event(db_event)
        for db_event in db_client.fetch_game_events(game_uuid)
    ]

    if not events:
        raise HTTPException(status_code=404, detail="Game not found")

    return events
