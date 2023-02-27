import asyncio
import logging
import os
import platform

from src.core.config import settings
from src.core.engine import GameEngine
from src.core.enums import SupportedSubs, UserBlacklist
from src.db.session import SessionLocal
from src.repositories import GameRepository, PlayerRepository, SubRedditRepository
from src.services import GameService, PlayerService, SubRedditService
from src.services.stream.inbox import InboxStreamService
from src.services.tag import TagService


logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

logger = logging.getLogger(__name__)
platform_name = platform.uname()


async def tag_init(subreddit_name: str = SupportedSubs.TAG_YOURE_IT_BOT) -> None:
    """Initialize a game of Tag for a subreddit

    :param subreddit_name:
        Display name of the subreddit to enable tag for
    :return:
        None
    """
    # TODO: i dont think this is the right way to do this. probably want
    # want to create new db connection for each processed message
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
        )

        logger.info(f"Game of Tag has started for SubReddit[r/{subreddit_name}]")
        await e.run()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    tasks = []
    supported_subs = (
        SupportedSubs.all()
        if settings.USERNAME == UserBlacklist.TAG_YOURE_IT_BOT
        else SupportedSubs.test()
    )

    for sub in supported_subs:
        task = loop.create_task(tag_init(subreddit_name=sub))
        tasks.append(task)

    loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()
