from uuid import UUID

from pydantic import BaseModel


class PlayerGetMeResponse(BaseModel):
    uuid: UUID
