import asyncio
import logging
import os
import platform
from typing import Optional

from src.core.config import settings
from src.core.engine import GameEngine
from src.core.enums import SupportedSubs
from src.db.session import SessionLocal
from src.repositories import GameRepository, PlayerRepository, SubRedditRepository
from src.services import GameService, PlayerService, SubRedditService
from src.services.stream.inbox import InboxStreamService
from src.services.tag import TagService


logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

platform_name = platform.uname()


async def tag_run(subreddit_name: Optional[str] = SupportedSubs.TAG_YOURE_IT_BOT) -> None:
    async with SessionLocal() as session:
        player_repo = PlayerRepository(db=session)
        game_repo = GameRepository(db=session)
        subreddit_repo = SubRedditRepository(db=session)
        e = GameEngine(
            stream_service=InboxStreamService(subreddit_name=subreddit_name),
            tag_service=TagService(
                player=PlayerService(repo=player_repo),
                game=GameService(repo=game_repo),
                subreddit=SubRedditService(repo=subreddit_repo),
            ),
            reddit_config={
                "client_id": settings.CLIENT_ID,
                "client_secret": settings.CLIENT_SECRET,
                "username": settings.USERNAME,
                "password": settings.PASSWORD,
                "user_agent": f"{platform_name}/{settings.VERSION} ({settings.BOT_NAME} {settings.DEVELOPER});",
            },
        )

        await e.run()


if __name__ == "__main__":
    asyncio.run(tag_run())
