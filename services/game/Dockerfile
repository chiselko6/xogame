# pull official base image
FROM python:3.8.6

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH=/root/.poetry/bin/:$PATH
RUN poetry config virtualenvs.create false

# install dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev

# copy project
COPY db/ db/
COPY domain/ domain/
COPY endpoints/ endpoints/
COPY clients/ clients/
COPY service.py settings.py ./

COPY ./entrypoint.sh .

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
