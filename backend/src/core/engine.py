import logging
from typing import Optional, Union
from uuid import UUID

from src.core.config import settings
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
    ):
        self.tag_service = tag_service
        self.stream_service = stream_service

    async def run(self) -> None:
        logger.info(
            f"Starting session with [{self.stream_service.__class__.__name__}] stream class for u/{settings.USERNAME}..."
        )
        game_id: Optional[Union[UUID, str]] = None
        tag_service: TagService = self.tag_service

        # TODO: move to decorator?
        try:
            async for mention in self.stream_service.client.stream():
                # pass
                pre_flight_check: bool = await self.stream_service.pre_flight_check(
                    tag_service, mention
                )
                if pre_flight_check:
                    game_id = await self.stream_service.process(tag_service, mention, game_id)

                    await mention.mark_read()
        finally:
            await self.stream_service.client.close()
