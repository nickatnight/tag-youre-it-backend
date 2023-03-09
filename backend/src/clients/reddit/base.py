import platform

import asyncpraw

from src.core.config import settings
from src.interfaces.client import IClient


platform_name = platform.uname()
USER_AGENT: str = f"{platform_name}/{settings.VERSION} ({settings.BOT_NAME} {settings.DEVELOPER});"


class RedditResource(IClient[asyncpraw.Reddit]):
    reddit: asyncpraw.Reddit

    @classmethod
    def configure(cls) -> asyncpraw.Reddit:
        reddit_config = {
            "client_id": settings.CLIENT_ID,
            "client_secret": settings.CLIENT_SECRET,
            "username": settings.USERNAME,
            "password": settings.PASSWORD,
            "user_agent": USER_AGENT,
        }
        return asyncpraw.Reddit(**reddit_config)

    async def close(self) -> None:
        """Close requester"""
        _ = await self.reddit.close()
