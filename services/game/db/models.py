from .base import Base
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy import Column, DateTime, String, UniqueConstraint, Integer


class Eventlog(Base):
    __table_args__ = (
        UniqueConstraint("game_uuid", "sequence"),
    )

    id = Column(Integer, primary_key=True)
    game_uuid = Column(UUID, nullable=False)
    name = Column(String(40), nullable=False)
    sequence = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    player_uuid = Column(UUID, nullable=False)
    params = Column(JSON, nullable=False)
