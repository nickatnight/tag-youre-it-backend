from typing import AsyncIterator

from asyncpraw.models import Message

from src.clients.reddit.base import RedditResource


class InboxClient(RedditResource):
    def __init__(self) -> None:
        self.reddit = self.configure()

    def stream(self) -> AsyncIterator[Message]:
        """stream incoming messages"""
        s: AsyncIterator[Message] = self.reddit.inbox.stream()

        return s

    async def close(self) -> None:
        """Close requester"""
        _ = await self.reddit.close()
