import logging
from datetime import datetime, timezone
from typing import List, Optional

from asyncpraw.models import Redditor

from src.core.exceptions import ObjectNotFound
from src.models.player import Player
from src.repositories.player import PlayerRepository
from src.schemas.player import IPlayerCreate, IPlayerUpdate
from src.services.base import BaseService


logger: logging.Logger = logging.getLogger(__name__)


class PlayerService(BaseService[PlayerRepository]):
    def __init__(self, repo: PlayerRepository) -> None:
        self.repo = repo

    async def list_opted_out(self) -> List[str]:
        players: List[Player] = await self.repo.f(**{"opted_out": True})

        return [p.username for p in players]

    async def set_opted_out(self, reddit_id: str, value: bool) -> None:
        player: Optional[Player] = await self.repo.get(**{"reddit_id": reddit_id})
        if not player:
            raise ObjectNotFound

        player_obj = IPlayerUpdate(opted_out=value)
        _ = await self.repo.update(player, player_obj)

        logger.info(f"[{player.username}] opted out of playing.")

    async def get_or_create(self, reddit_obj: Redditor) -> Player:
        player_obj = IPlayerCreate(
            username=reddit_obj.name,
            reddit_id=reddit_obj.id,
            icon_img=reddit_obj.icon_img,
            is_employee=reddit_obj.is_employee,
            created_utc=reddit_obj.created_utc,
            verified=reddit_obj.verified,
            is_suspended=reddit_obj.is_suspended if hasattr(reddit_obj, "is_suspended") else False,
            has_verified_email=reddit_obj.has_verified_email,
        )
        instance = await self.repo.get_or_create(
            player_obj, **{"username": reddit_obj.name}
        )

        return instance

    async def untag(self, reddit_obj: Redditor) -> None:
        instance = await self.get_or_create(reddit_obj)

        player_obj = IPlayerUpdate(tag_time=None)
        _ = await self.repo.update(instance, player_obj)

    async def tag(self, reddit_obj: Redditor) -> None:
        instance = await self.get_or_create(reddit_obj)

        player_obj = IPlayerUpdate(tag_time=datetime.now(timezone.utc))
        _ = await self.repo.update(instance, player_obj)
