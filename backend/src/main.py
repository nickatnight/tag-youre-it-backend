import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from src.api import routes
from src.api.deps import get_redis_client
from src.core.config import settings
from src.db.session import add_postgresql_extension


logger = logging.getLogger(__name__)

if settings.USE_SENTRY is True:
    import sentry_sdk

    logger.info("Initializing Sentry...")
    sentry_sdk.init(
        dsn="https://f206851df3fd40ecabdf48f812cde72d@o4504749978681344.ingest.sentry.io/4504749981368320",
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0,
    )

tags_metadata = [
    {
        "name": "health",
        "description": "Health check for api",
    },
    {
        "name": "games",
        "description": "List of Games",
    },
    {
        "name": "players",
        "description": "List of Players",
    },
    {
        "name": "subreddits",
        "description": "List of SubReddits",
    },
]

origins = [
    "https://tagyoureitbot.com",
    "http://localhost",
    "http://localhost:3000",
]

app = FastAPI(
    title="tag-youre-it-backend",
    description="Backend for TagYoureIt Reddit bot",
    version=settings.VERSION,
    openapi_url=f"/{settings.VERSION}/openapi.json",
    openapi_tags=tags_metadata,
)


async def on_startup() -> None:
    await add_postgresql_extension()
    redis_client = await get_redis_client()
    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")
    logger.info("FastAPI app running...")


app.add_middleware(CORSMiddleware, allow_origins=origins, expose_headers=["x-content-range"])

app.add_event_handler("startup", on_startup)

app.include_router(routes.home_router)
app.include_router(routes.api_router, prefix=f"/{settings.VERSION}")
