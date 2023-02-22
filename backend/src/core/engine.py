import copy
import logging
from typing import Optional, Union
from uuid import UUID

import asyncpraw
from aiohttp import ClientSession

from src.core.config import settings
from src.core.typed import RedditClientConfigTyped
from src.services.stream.comment import CommentStreamService
from src.services.stream.inbox import InboxStreamService
from src.services.tag import TagService


logger = logging.getLogger(__name__)


#   _______              __     __         _               _____ _
#  |__   __|             \ \   / /        ( )             |_   _| |
#     | | __ _  __ _ _____\ \_/ /__  _   _|/ _ __ ___ ______| | | |_
#     | |/ _` |/ _` |______\   / _ \| | | | | '__/ _ \______| | | __|
#     | | (_| | (_| |       | | (_) | |_| | | | |  __/     _| |_| |_
#     |_|\__,_|\__, |       |_|\___/ \__,_| |_|  \___|    |_____|\__|
#               __/ |
#              |___/
class GameEngine:
    """main class for game...max one instance of GameEngine per Subreddit"""

    def __init__(
        self,
        tag_service: TagService,
        stream_service: Union[InboxStreamService, CommentStreamService],
        reddit_config: RedditClientConfigTyped,
    ):
        self.tag_service = tag_service
        self.stream_service = stream_service
        self.reddit_config = reddit_config

    async def run(self) -> None:
        logger.info(
            f"Starting session with [{self.stream_service.__class__.__name__}] stream class..."
        )
        async with ClientSession(trust_env=True) as session:
            config: RedditClientConfigTyped = copy.deepcopy(self.reddit_config)
            config.update(
                {
                    "requestor_kwargs": {
                        "session": session
                    },  # must successfully close the session when finished
                }
            )
            game_id: Optional[Union[UUID, str]] = None
            tag_service: TagService = self.tag_service

            async with asyncpraw.Reddit(**self.reddit_config) as reddit:
                logger.info(f"Streaming mentions for u/{settings.USERNAME}")

                async for mention in self.stream_service.stream(reddit):
                    # pass
                    pre_flight_check: bool = await self.stream_service.pre_flight_check(
                        tag_service, mention
                    )
                    if pre_flight_check:
                        game_id = await self.stream_service.process(tag_service, mention, game_id)

                        await mention.mark_read()
