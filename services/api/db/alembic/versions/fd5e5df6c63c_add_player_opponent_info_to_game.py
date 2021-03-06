"""add player_opponent info to game

Revision ID: fd5e5df6c63c
Revises: 492408566602
Create Date: 2021-04-05 14:37:57.803226

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "fd5e5df6c63c"
down_revision = "492408566602"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "game", sa.Column("player_opponent", postgresql.UUID(), nullable=True)
    )
    op.create_foreign_key(
        "game_opponent_player_uuid_fk", "game", "player", ["player_opponent"], ["uuid"]
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("game_opponent_player_uuid_fk", "game", type_="foreignkey")
    op.drop_column("game", "player_opponent")
    # ### end Alembic commands ###
