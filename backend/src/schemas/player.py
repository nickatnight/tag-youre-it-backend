from datetime import datetime
from typing import List, Optional
from uuid import UUID

from src.core.utils import optional
from src.models.game import Game
from src.models.player import PlayerBase


class IPlayerCreate(PlayerBase):
    pass


class IPlayerRead(PlayerBase):
    created_at: datetime
    ref_id: UUID
    games: Optional[List[Game]] = []


@optional
class IPlayerUpdate(PlayerBase):
    pass
