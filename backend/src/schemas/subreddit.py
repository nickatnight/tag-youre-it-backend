from typing import List, Optional
from uuid import UUID

from src.core.utils import optional
from src.models.game import GameBase
from src.models.subreddit import SubRedditBase


class ISubRedditCreate(SubRedditBase):
    pass


class ISubRedditRead(SubRedditBase):
    ref_id: UUID
    games: Optional[List[GameBase]]


@optional
class ISubRedditUpdate(SubRedditBase):
    pass
