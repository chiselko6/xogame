#!/bin/bash

alembic --config db/alembic.ini upgrade head && uvicorn service:app --host 0.0.0.0