import platform

import asyncpraw

from src.core.config import settings
from src.interfaces.client import IClient


class RedditResource(IClient[asyncpraw.Reddit]):
    @classmethod
    def configure(cls) -> asyncpraw.Reddit:
        platform_name = platform.uname()
        reddit_config = {
            "client_id": settings.CLIENT_ID,
            "client_secret": settings.CLIENT_SECRET,
            "username": settings.USERNAME,
            "password": settings.PASSWORD,
            "user_agent": f"{platform_name}/{settings.VERSION} ({settings.BOT_NAME} {settings.DEVELOPER});",
        }
        return asyncpraw.Reddit(**reddit_config)
