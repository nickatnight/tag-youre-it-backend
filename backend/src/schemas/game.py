from datetime import datetime
from typing import List, Optional
from uuid import UUID

from src.core.utils import optional
from src.models.game import GameBase
from src.models.player import Player
from src.models.subreddit import SubReddit


class IGameCreate(GameBase):
    pass


class IGameRead(GameBase):
    created_at: datetime
    ref_id: UUID
    subreddit: Optional[SubReddit] = None
    players: Optional[List[Player]] = []


@optional
class IGameUpdate(GameBase):
    pass
