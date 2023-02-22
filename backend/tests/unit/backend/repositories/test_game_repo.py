import pytest
from mock import Mock

from src.interfaces.repository import IRepository
from src.models.game import Game
from src.models.player import Player
from src.services.game import GameService
from src.services.player import PlayerService
from src.services.subreddit import SubRedditService
from tests.unit import test_subreddit


PLAYER_TWO = {
    "name": "test",
    "is_employee": False,
    "id": "fs89dfd",
    "icon_img": "test.com",
    "created_utc": 1626226832.0,
    "verified": False,
    "is_suspended": False,
    "has_verified_email": False,
}


@pytest.mark.asyncio
async def test_create_game(
    game_repo: IRepository,
    sub_repo: IRepository,
    player_repo: IRepository,
    player: Player,
):
    player_service = PlayerService(repo=player_repo)
    sub_service = SubRedditService(repo=sub_repo)

    mock_sub = Mock()
    mock_sub.configure_mock(**test_subreddit)

    mock_player = Mock()
    mock_player.configure_mock(**PLAYER_TWO)

    sub = await sub_service.get_or_create(mock_sub)
    p2 = await player_service.get_or_create(mock_player)

    game_service = GameService(repo=game_repo)
    instance = await game_service.new(sub, player, p2)

    assert type(instance) == Game

    player_names = [p.username for p in instance.players]
    assert player.username in player_names
    assert p2.username in player_names
