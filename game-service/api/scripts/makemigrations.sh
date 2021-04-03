env $(cat .env | xargs) poetry run alembic --config db/alembic.ini revision --autogenerate -m "$1"
