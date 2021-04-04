#!/bin/bash

#alembic --config db/alembic.ini upgrade head && uvicorn service:app
uvicorn service:app