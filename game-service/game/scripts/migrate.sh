env $(cat .env | xargs) poetry run alembic --config db/alembic.ini upgrade head
