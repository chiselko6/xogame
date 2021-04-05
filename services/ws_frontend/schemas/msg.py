from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel


class WSResponse(BaseModel):
    ok: bool
    error: Optional[str]


class BroadcastEvent(BaseModel):
    name: str
    game_uuid: UUID
    sequence: int
    player_uuid: UUID
    timestamp: datetime
    params: Dict[str, Any]
