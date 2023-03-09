from typing import AsyncIterator

from asyncpraw.models import Message

from src.clients.reddit.base import RedditResource


class InboxClient(RedditResource):
    def __init__(self, reddit=None) -> None:
        self.reddit = reddit or self.configure()

    def stream(self) -> AsyncIterator[Message]:
        """stream incoming messages"""
        s: AsyncIterator[Message] = self.reddit.inbox.stream()

        return s

    async def close(self) -> None:
        """Close requester"""
        await self.reddit.close()
