from .base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, DateTime, String, UniqueConstraint


class Player(Base):
    __table_args__ = (
        UniqueConstraint("username"),
    )

    uuid = Column(UUID, primary_key=True)
    date_joined = Column(DateTime, nullable=False)
    username = Column(String(40), nullable=False)


class User(Base):
    username = Column(String(40), primary_key=True)
    password = Column(String(250), nullable=False)
