env $(cat .env | xargs) poetry run uvicorn service:app
