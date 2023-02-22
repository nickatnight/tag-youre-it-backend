import logging
from datetime import datetime, timezone
from typing import List, Optional, Union
from uuid import UUID

from asyncpraw.models import Redditor
from asyncpraw.models import Subreddit as PrawSubReddit

from src.core.exceptions import ObjectNotFound
from src.models.game import Game
from src.models.player import Player
from src.models.subreddit import SubReddit
from src.schemas.game import IGameUpdate
from src.schemas.player import IPlayerUpdate
from src.services.game import GameService
from src.services.player import PlayerService
from src.services.subreddit import SubRedditService


logger: logging.Logger = logging.getLogger(__name__)


class TagService:
    """main service for all Tag operations"""

    def __init__(self, player: PlayerService, game: GameService, subreddit: SubRedditService):
        self.player = player
        self.game = game
        self.subreddit = subreddit

    async def reset_game(self, game_ref_id: Union[UUID, str], tagger: Player) -> None:
        logger.info(f"Player [{tagger.username}] tag time expired. Ending game.")
        game_obj = IGameUpdate(is_active=False)
        db_obj: Optional[Game] = await self.game.repo.get(**{"ref_id": game_ref_id})

        if not db_obj:
            raise ObjectNotFound(f"Game[{game_ref_id}] not found")

        _ = await self.game.repo.update(db_obj, game_obj)

        player_obj = IPlayerUpdate(tag_time=None)
        await self.player.repo.update(tagger, player_obj)

    async def current_game(self, subreddit: SubReddit) -> Optional[Game]:
        active_games: List[Game] = await self.game.active()

        for game in active_games:
            if game.subreddit_id == subreddit.id:
                return game

        return None

    def it_player(self, game: Game) -> Player:
        logger.info(f"Fetching 'it' Player for Game[{game.ref_id}]")

        # TODO: either prevent a player from tagging someone in a differnet sub
        # while 'it' or add new field to determine when tagged
        players: List[Player] = [p for p in game.players if p.tag_time]
        sorted_playes: List[Player] = sorted(
            players, key=lambda p: p.tag_time, reverse=True  # type: ignore
        )

        if not sorted_playes:
            raise ObjectNotFound(f"Could not find 'it' Player for Game[{game.ref_id}]")

        return sorted_playes[0]

    async def add_player_to_game(self, game_ref_id: Union[UUID, str], tagee: Player) -> None:
        game_ref_ids: List[str] = [str(g.ref_id) for g in tagee.games]
        tagge_obj = IPlayerUpdate(tag_time=datetime.now(timezone.utc))

        await self.player.repo.update(tagee, tagge_obj)

        if str(game_ref_id) in game_ref_ids:
            logger.info(f"Player[{tagee.username}] already exists in Game[{game_ref_id}]")
            return

        await self.game.add_player(tagee, game_ref_id)

    async def game_create(self, subreddit: SubReddit, tagger: Player, tagee: Player) -> Game:
        g: Game = await self.game.new(subreddit, tagger, tagee)
        return g

    async def player_get_or_create(self, reddit_obj: Redditor) -> Player:
        p: Player = await self.player.get_or_create(reddit_obj)
        return p

    async def player_tag(self, reddit_obj: Redditor) -> None:
        await self.player.tag(reddit_obj)

    async def player_untag(self, reddit_obj: Redditor) -> None:
        """untag tagger for safety check

        they could have been the last person tagged in a previous game
        """
        await self.player.untag(reddit_obj)

    async def player_list_opted_out(self) -> List[str]:
        opt_list: List[str] = await self.player.list_opted_out()
        return opt_list

    async def player_set_opted_out(self, reddit_id: str, value: bool) -> None:
        await self.player.set_opted_out(reddit_id, value)

    async def subreddit_get_or_create(self, reddit_obj: PrawSubReddit) -> SubReddit:
        sub: SubReddit = await self.subreddit.get_or_create(reddit_obj)
        return sub
