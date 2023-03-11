import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.models.game import Game
from src.models.player import Player
from src.models.subreddit import SubReddit
from src.services.tag import TagService


@pytest_asyncio.fixture(autouse=True)
async def setup(async_session, player, it_player, subreddit):
    async_session.add(player)
    async_session.add(it_player)
    async_session.add(subreddit)
    await async_session.commit()

    await async_session.refresh(player)
    await async_session.refresh(it_player)
    await async_session.refresh(subreddit)

    game = Game(subreddit_id=subreddit.id)
    async_session.add(game)
    await async_session.commit()
    await async_session.refresh(game)

    game.players.append(player)
    game.players.append(it_player)
    await async_session.commit()

    yield


class TestTagService:
    @pytest.mark.asyncio
    async def test_reset_game(self, async_session: AsyncSession, mock_tag_service: TagService):
        player_response = await async_session.execute(
            select(Player).where(Player.reddit_id == "testid")
        )
        p = player_response.scalar_one()
        game_response = await async_session.execute(select(Game))
        g = game_response.scalars().all()[0]

        assert g.is_active is True
        await mock_tag_service.reset_game(g.ref_id, p)

        assert g.is_active is False

    @pytest.mark.asyncio
    async def test_current_game(self, mock_tag_service: TagService, subreddit: SubReddit):
        game = await mock_tag_service.current_game(subreddit)
        assert game.subreddit.sub_id == subreddit.sub_id

    @pytest.mark.asyncio
    async def test_add_player_to_game(
        self, async_session: AsyncSession, fake_player: Player, mock_tag_service: TagService
    ):
        async_session.add(fake_player)
        await async_session.commit()
        await async_session.refresh(fake_player)

        game_response = await async_session.execute(select(Game))
        g = game_response.scalars().all()[0]

        await mock_tag_service.add_player_to_game(g.ref_id, fake_player)

        assert fake_player in g.players

    @pytest.mark.asyncio
    async def test_it_player(self, async_session: AsyncSession, mock_tag_service: TagService):
        game_response = await async_session.execute(select(Game))
        g = game_response.scalars().all()[0]

        it = mock_tag_service.it_player(g)

        assert it.username == "iamitplayer"
