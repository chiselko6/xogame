from pydantic import BaseModel
from datetime import datetime
from typing import ClassVar, Dict, Any
from uuid import UUID


class BaseEvent(BaseModel):
    name: ClassVar

    sequence: int
    player_uuid: UUID
    timestamp: datetime
    params: BaseModel
