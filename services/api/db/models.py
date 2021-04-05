from sqlalchemy import (Column, DateTime, ForeignKeyConstraint, String,
                        UniqueConstraint)
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class User(Base):
    username = Column(String(40), primary_key=True)
    password = Column(String(250), nullable=False)


class Player(Base):
    __table_args__ = (
        UniqueConstraint("username"),
        ForeignKeyConstraint(
            columns=("username",),
            refcolumns=(User.username,),
            name="player_username_user_username_fk",
        ),
    )

    uuid = Column(UUID, primary_key=True)
    date_joined = Column(DateTime, nullable=False)
    username = Column(String(40), nullable=False)


class Game(Base):
    __table_args__ = (
        ForeignKeyConstraint(columns=("player_created",), refcolumns=(Player.uuid,)),
        ForeignKeyConstraint(
            columns=("player_opponent",),
            refcolumns=(Player.uuid,),
            name="game_opponent_player_uuid_fk",
        ),
    )

    uuid = Column(UUID, primary_key=True)
    date_created = Column(DateTime, nullable=False)
    player_created = Column(UUID, nullable=False)
    player_opponent = Column(UUID, nullable=True)
