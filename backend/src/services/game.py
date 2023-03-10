import logging
from typing import Optional, Union
from uuid import UUID

from sqlmodel import select

from src.core.exceptions import ObjectNotFound
from src.models.game import Game
from src.models.player import Player
from src.models.subreddit import SubReddit
from src.repositories.game import GameRepository
from src.schemas.game import IGameCreate
from src.services.base import BaseService


logger: logging.Logger = logging.getLogger(__name__)


class GameService(BaseService[GameRepository]):
    def __init__(self, repo: GameRepository) -> None:
        self.repo = repo

    async def new(self, subreddit: SubReddit, tagger: Player, tagee: Player) -> Game:
        game_obj = IGameCreate(subreddit_id=subreddit.id)
        instance = await self.repo.create(game_obj)
        logger.info(f"New r/{subreddit.display_name} Game[{instance.ref_id}]")

        await self.add_player(tagger, instance.ref_id)
        await self.add_player(tagee, instance.ref_id)

        return instance

    async def add_player(self, player: Player, game_ref_id: Union[UUID, str]) -> None:
        game: Optional[Game] = await self.repo.get(**{"ref_id": game_ref_id})
        if not game:
            raise ObjectNotFound
        game.players.append(player)

        await self.repo.db.commit()
        await self.repo.db.refresh(game)

        logger.info(f"Adding Players[{player.username}] to Game[{game.ref_id}]")

    async def active(self, sub: SubReddit) -> Optional[Game]:
        logger.info("Fetching current game")
        statement = (
            select(self.repo._model)
            .where(self.repo._model.is_active == True)  # noqa
            .where(self.repo._model.subreddit_id == sub.id)
            .order_by(self.repo._model.__table__.columns["created_at"].desc())  # type: ignore
        )
        results = await self.repo.db.execute(statement)
        game: Optional[Game] = results.scalar_one_or_none()

        if not game:
            logger.info(f"No Game found for sub[{sub.ref_id}]")

        return game
