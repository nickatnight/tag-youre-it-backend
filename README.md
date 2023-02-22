<p align="center">
    <a href="https://github.com/nickatnight/tag-youre-it-backend/actions">
        <img alt="GitHub Actions status" src="https://github.com/nickatnight/tag-youre-it-backend/actions/workflows/main.yml/badge.svg">
    </a>
    <a href="https://codecov.io/gh/nickatnight/tag-youre-it-backend">
        <img alt="Coverage" src="https://codecov.io/gh/nickatnight/tag-youre-it-backend/branch/main/graph/badge.svg?token=E03I4QK6D9"/>
    </a>
    <a href="https://github.com/nickatnight/tag-youre-it-backend/releases"><img alt="Release Status" src="https://img.shields.io/github/v/release/nickatnight/tag-youre-it-backend"></a>
    <a href="https://github.com/nickatnight/tag-youre-it-backend/blob/master/LICENSE">
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

c) Showcase the ecosystem of my open source projects and how they work together: [Create Release GHA](https://github.com/nickatnight/releases-action), [FastAPI Backend Base](https://github.com/nickatnight/fastapi-backend-base), [Reddit Bot Base](https://github.com/nickatnight/docker-reddit-bot-base).

d) I'm curious to see stats of user engagement (how long did a game chain last, how many users did it contain, which subreddit plays the most, etc)

See [r/TagYoureItBot](https://www.reddit.com/r/TagYoureItBot) for more updates.
## Architecture
<p align="center">
    <a href="#">
        <img alt="Architecture Workflow" src="https://i.imgur.com/8TEpVZk.png">
    </a>
</p>

## Usage
1. `make up`
2. visit `http://localhost:8666/v1/ping` for uvicorn server, or `http://localhost` for nginx server
3. Backend, JSON based web API based on OpenAPI: `http://localhost/v1/`
4. Automatic interactive documentation with Swagger UI (from the OpenAPI backend): `http://localhost/docs`

## Backend local development, additional details

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

### General workflow
See the [Makefile](/Makefile) to view available commands.

By default, the dependencies are managed with [Poetry](https://python-poetry.org/), go there and install it.

From `./backend/` you can install all the dependencies with:

```console
$ poetry install
```

### pre-commit hooks
If you haven't already done so, download [pre-commit](https://pre-commit.com/) system package and install. Once done, install the git hooks with
```console
$ pre-commit install
pre-commit installed at .git/hooks/pre-commit
```

### Nginx
The Nginx webserver acts like a web proxy, or load balancer rather. Incoming requests can get proxy passed to various upstreams eg. `/:service1:8001,/static:service2:8002`

```yml
volumes:
  proxydata-vol:
...
nginx:
    image: your-registry/nginx
    # OR you can do the following
    # build:
    #   context: ./nginx
    #   dockerfile: ./Dockerfile
    environment:
      - UPSTREAMS=/:backend:8000
      - NGINX_SERVER_NAME=yourservername.com
      - ENABLE_SSL=true
      - HTTPS_REDIRECT=true
      - CERTBOT_EMAIL=youremail@gmail.com
      - DOMAIN_LIST=yourservername.com
      - BASIC_AUTH_USER=user
      - BASIC_AUTH_PASS=pass
    ports:
      - '0.0.0.0:80:80'
      - '0.0.0.0:443:443'
    volumes:
      - proxydata-vol:/etc/letsencrypt
```

Some of the environment variables available:
- `UPSTREAMS=/:backend:8000` a comma separated list of \<path\>:\<upstream\>:\<port\>.  Each of those of those elements creates a location block with proxy_pass in it.
- `HTTPS_REDIRECT=true` enabled a standard, ELB compliant https redirect.
- `ENABLE_SSL=true` to enable redirects to https from http
- `NGINX_SERVER_NAME` name of the server and used as path name to store ssl fullchain and privkey
- `CERTBOT_EMAIL=youremail@gmail.com` the email to register with Certbot.
- `DOMAIN_LIST` domain(s) you are requesting a certificate for.
- `BASIC_AUTH_USER` username for basic auth.
- `BASIC_AUTH_PASS` password for basic auth.

When SSL is enabled, server will install Cerbot in standalone mode and add a new daily periodic script to `/etc/periodic/daily/` to run a cronjob in the background. This allows you to automate cert renewing (every 3 months). See [docker-entrypoint](nginx/docker-entrypoint.sh) for details.
### Deployments
A common scenario is to use an orchestration tool, such as docker swarm, to deploy your containers to the cloud (DigitalOcean). This can be automated via GitHub Actions workflow. See [main.yml](/.github/workflows/main.yml) for more.

You will be required to add `secrets` in your repo settings:
- DIGITALOCEAN_TOKEN: your DigitalOcean api token
- REGISTRY: container registry url where your images are hosted
- POSTGRES_PASSWORD: password to postgres database
- STAGING_HOST_IP: ip address of the staging droplet
- PROD_HOST_IP: ip address of the production droplet
- SSH_KEY: ssh key of user connecting to server

Made with :heart: from Cali
