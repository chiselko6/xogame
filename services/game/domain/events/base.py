import json
from datetime import datetime
from typing import ClassVar
from uuid import UUID

from pydantic import BaseModel


class BaseEvent(BaseModel):
    name: ClassVar

    game_uuid: UUID
    sequence: int
    player_uuid: UUID
    timestamp: datetime
    params: BaseModel

    def json(self, *args, **kwargs) -> str:
        return json.dumps(
            {
                "name": self.name,
                **json.loads(super().json(*args, **kwargs)),
            }
        )
