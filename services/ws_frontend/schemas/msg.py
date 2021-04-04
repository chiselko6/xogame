from pydantic import BaseModel
from typing import Optional, Dict, Any
from uuid import UUID


class WSResponse(BaseModel):
    ok: bool
    error: Optional[str]


class BroadcastMessage(BaseModel):
    game_uuid: UUID
    payload: Dict[str, Any]
