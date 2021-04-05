from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel


class WSResponse(BaseModel):
    ok: bool
    error: Optional[str]


class BroadcastMessage(BaseModel):
    game_uuid: UUID
    payload: Dict[str, Any]
