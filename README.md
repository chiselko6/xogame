# xogame

```
___   ___   ______        _______      ___      .___  ___.  _______ 
\  \ /  /  /  __  \      /  _____|    /   \     |   \/   | |   ____|
 \  V  /  |  |  |  |    |  |  __     /  ^  \    |  \  /  | |  |__   
  >   <   |  |  |  |    |  | |_ |   /  /_\  \   |  |\/|  | |   __|  
 /  .  \  |  `--'  |    |  |__| |  /  _____  \  |  |  |  | |  |____ 
/__/ \__\  \______/      \______| /__/     \__\ |__|  |__| |_______|
```

Multiplayer XO game in Python

## Table of contents

* [Architecture](#architecture)
* [API](#api)
* [Local deployment](#local-deployment)
* [Frameworks and libraries used](#frameworks-and-libraries-used)
* [Critical path](#critical-path)

### Architecture

The application is represented with 3 services:

- API service - contains information about users (each user has an object assigned - player, which is referenced in the games), games (only meta information).
- Game service - for processing game events. Currently game commands include: GameInitCommand and MoveCommand.
This is a pure event sourcing (all games are defined by a sequence of stored events) with elements of CQRS (to modify the state the client needs to the send a corresponding command, though currently the latest state is fetched by events, however, it is fairly easy to add another endpoint to fetch the resulting state).
- WS service - the service to hold persistent websocket connections.
This validates the commands to be applied to the authorized game only and redirects them to the Game service.
What is more, it is responsible for broadcasting the events (e.g. when one user do the move, it notifies the opponent about it).

Bot logic is not implemented in the project, but there is no real blockers for it.
For example, it can be implemented as a part of processing the incoming command.

API service and Game service are hidden by Nginx.

Services communicate via HTTP messages.

### API

As the project uses a [FastAPI](https://fastapi.tiangolo.com/) library, it comes with a predefined API generator (available at `/docs` for each app).
It is not a part of README as one can view it when the app is deployed.

### Local deployment

All services are built with Docker and have a `docker-compose.yaml` file.
Moreover, there is a global `docker-compose.yaml`, which builds and starts all required infrastructure.

To correctly produce the build, a developer needs to modify `.env.example` in each project to produce `.env` file with the right creds.

### Frameworks and libraries used

- [Pydantic](https://pydantic-docs.helpmanual.io/) - for request/response schemas and ORM objects.
- [FastAPI](https://fastapi.tiangolo.com/) - easy-to-use framework for web apps. Comes with a great tooling and other libraries (pydantic, websockets, DI)
- [aiohttp](https://docs.aiohttp.org/en/stable/) - for intraservice communication.

### Critical path

Here is a sequence of calls that the client needs to make to authorize and play a game (with description):

1. Login. Here we assume that somehow users are signed up (we don't care currently for now how exactly).

```
curl <api_service>/auth/login -X GET -d 'username=<username>&password=<password>' -H 'content-type: application/x-www-form-urlencoded'
Response: {"access_token": <auth_token>, "type": "Bearer"}
```

Auth bearer token is the one required to make any authorized calls to the API service.

1. Create a new game. This is called when the user creates a game to play with anyone.

```
curl <api_service>/game/ -X POST -H 'authorization: Bearer <auth_token>'
Response: {"uuid": <game_uuid>}
```

This sets the created game as a waiting one.

1. When another player wants to play, he fetches a list of games in "waiting" status.

```
curl <api_service>/game/awaiting -H 'authorization: Bearer <auth_token>'
Response: {"games": [{"uuid": <game_uuid>, "date_created": ..., "player_created": <player_created>}, ...]}
```

He then selects the interesting one (the created game params should be displayed here and specified in the previous step, but it is not implemented now) and connects to it.

1. In order to connect to a particular game, the client needs 1) to fetch information about himself).

```
curl <api_service>/player/me -H 'authorization: Bearer <auth_token>'
Response: {"uuid": <player_id>}
```

Basically we can include username information in the requests to the game service, but currently it is done via player uuid (we would allow users to change their username).

1. In order to connect to a particular game, the client needs 2) to obtain an intratoken, which will be used to authenticate to a particular game.

```
curl <api_service>/intratoken/<game_id> -H 'authorization: Bearer <auth_token>'
Response: {"access_token": <intratoken>, "type": "Intra"}
```

1. Connect to the game service. This opens a websocket connection with two-way messages (with broadcasts).

Target host: `<ws_frontend_service>/ws`.

The first thing to do with the open websocket connection is to authorize:

```
>>> {"type": "authorize", "data": {"token": <intratoken>}}
<<< {"ok": true, "error": null}
```

From now on, the client can send messages to the service (e.g. commands), but only for the current game_id (which is encoded in the intratoken).

That's it! You can send the commands.
