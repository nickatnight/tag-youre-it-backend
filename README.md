<p align="center">
    <a href="https://github.com/nickatnight/tag-youre-it-backend/actions">
        <img alt="GitHub Actions status" src="https://github.com/nickatnight/tag-youre-it-backend/actions/workflows/main.yml/badge.svg">
    </a>
    <a href="https://codecov.io/gh/nickatnight/tag-youre-it-backend">
        <img alt="Coverage" src="https://codecov.io/gh/nickatnight/tag-youre-it-backend/branch/main/graph/badge.svg?token=E03I4QK6D9"/>
    </a>
    <a href="https://github.com/nickatnight/tag-youre-it-backend/releases"><img alt="Release Status" src="https://img.shields.io/github/v/release/nickatnight/tag-youre-it-backend"></a>
    <a href="https://github.com/nickatnight/tag-youre-it-backend/releases"><img alt="Python Badge" src="https://img.shields.io/badge/python-3.8%7C3.9%7C3.10%7C3.11-blue"></a>
    <a href="https://github.com/nickatnight/tag-youre-it-backend/blob/main/LICENSE">
        <img alt="License Shield" src="https://img.shields.io/github/license/nickatnight/tag-youre-it-backend">
    </a>
</p>


# tag-youre-it-backend :runner:
<p align="center">
    <a href="https://c.tenor.com/Sf4IW_C95v4AAAAC/tag.gif"><img alt="tag" src="https://c.tenor.com/Sf4IW_C95v4AAAAC/tag.gif"></a>
</p>

FastAPI backend for Reddit's TagYoureItBot

Frontend - https://tagyoureitbot.com

API - https://api.tagyoureitbot.com/docs

Project was scaffolded with [cookiecutter-fastapi-backend](https://github.com/nickatnight/cookiecutter-fastapi-backend)

## How To Play (beta)
For now, this bot will only supports subreddit-level play (one active game per sub). This prevents trolls from locking a global game to a (private)subreddit (See the TODO for future enhancements):

Invoke `u/TagYoureItBot` by replying to a Reddit post or comment with the phrase `!tag` e.g. `u/TagYoureItBot !tag`. 1 of 2 things can happen:
- There is no active game. `u/TagYoureItBot` will reply to the same post or comment notifying the author they are now "it". A countdown will start and this author will have an allotted time to "tag" another Reddit user (within the same sub). If the countdown expires and the author has not tagged another user, the game will end. Otherwise...
- There is an active game. If you are the "it" user, the game will continue (see previous paragraph). If you're not it, the bot will reply to your comment stating such. The comment will include a countdown time of how much longer the current tagged user has to tag someone until the game automatically ends.


## Rules
You can't tag...
1. yourself
2. ~back....yet~
3. a user who has opted out of playing
4. u/TagYoureItBot

To opt out of playing, send `u/TagYoureItBot` a private message which contains 'i dont want to play tag' as the subject :heart:

If you would like to opt back in, send `u/TagYoureItBot` a private message with 'i want to play tag again' as the subject

## Why did I build this?
a) A few years ago I read a [reddit blog post](https://www.redditinc.com/blog/how-we-built-rplace/), where they outlined how r/Place was built. I got inspired by the community aspect of the project, and wanted to create something similar (obviously no where near the scale/volume). So I started to create a digital version of Tag that can be played on Reddit. I pushed a closed source v1 last year, but the game logic was coupled to the web api code (FastApi). I decided to decompose the bot logic into an open source package and keep the web api closed source.

b) Want keep my Python skills fresh since I've been doing a lot of full-stack development in my previous role (React/Java).

c) Showcase the ecosystem of my open source projects and how they work together: [Create Release GHA](https://github.com/nickatnight/releases-action), [FastAPI Backend Base](https://github.com/nickatnight/cookiecutter-fastapi-backend), [Reddit Bot Base](https://github.com/nickatnight/docker-reddit-bot-base).

d) I'm curious to see stats of user engagement (how long did a game chain last, how many users did it contain, which subreddit plays the most, etc)

See [r/TagYoureItBot](https://www.reddit.com/r/TagYoureItBot) for more updates.
## Architecture
<p align="center">
    <a href="#">
        <img alt="Architecture Workflow" src="https://i.imgur.com/YJjmgva.png">
    </a>
</p>

## Development
1. `make up`
2. visit `http://localhost:8666/v1/ping` for uvicorn server, or `http://localhost` for nginx server
3. Backend, JSON based web API based on OpenAPI: `http://localhost/v1/`
4. Automatic interactive documentation with Swagger UI (from the OpenAPI backend): `http://localhost/docs`

The entrypoint to the bot can be found in `src.core.bot`. In short, for each sub which the bot is enabled, an async process will be pushed onto the event loop (each sub gets their own game engine).

### Migrations

After adding some models in `src/models/`, you can run the initial making of the migrations
```console
$ make alembic-init
$ make alembic-migrate
```
Every migration after that, you can create new migrations and apply them with
```console
$ make alembic-make-migrations "cool comment dude"
$ make alembic-migrate
```

### pre-commit hooks
If you haven't already done so, download [pre-commit](https://pre-commit.com/) system package and install. Once done, install the git hooks with
```console
$ pre-commit install
pre-commit installed at .git/hooks/pre-commit
```

Made with :heart: from Cali
