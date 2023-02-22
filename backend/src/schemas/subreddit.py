from typing import List, Optional
from uuid import UUID

from src.core.utils import optional
from src.models.subreddit import SubRedditBase


class ISubRedditCreate(SubRedditBase):
    pass


class ISubRedditRead(SubRedditBase):
    ref_id: UUID
    games: Optional[List["Game"]] = []  # type: ignore # noqa


@optional
class ISubRedditUpdate(SubRedditBase):
    pass
