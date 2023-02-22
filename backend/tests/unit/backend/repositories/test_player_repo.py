from datetime import datetime, timezone

import pytest
from mock import Mock
from sqlalchemy.ext.asyncio import AsyncSession

from src.interfaces.repository import IRepository
from src.models.player import Player
from src.services.player import PlayerService
from tests.unit import test_redditor_one


@pytest.mark.asyncio
async def test_get_or_create_when_object_doesnt_exist(player_repo: IRepository):
    service = PlayerService(repo=player_repo)
    mock_redditor = Mock()
    mock_redditor.configure_mock(**test_redditor_one)
    instance = await service.get_or_create(mock_redditor)

    assert type(instance) == Player
    assert instance.username == test_redditor_one["name"]


@pytest.mark.asyncio
async def test_get_or_create_when_object_exists(
    async_session: AsyncSession, player_repo: IRepository, player: Player
):
    async_session.add(player)
    await async_session.commit()
    await async_session.refresh(player)

    service = PlayerService(repo=player_repo)
    mock_redditor = Mock()
    mock_redditor.configure_mock(**test_redditor_one)
    instance = await service.get_or_create(mock_redditor)

    assert instance.ref_id == player.ref_id


@pytest.mark.asyncio
async def test_tag(async_session: AsyncSession, player_repo: IRepository, player: Player):
    async_session.add(player)
    await async_session.commit()
    await async_session.refresh(player)

    assert player.tag_time is None

    service = PlayerService(repo=player_repo)
    mock_redditor = Mock()
    mock_redditor.configure_mock(**test_redditor_one)

    await service.tag(mock_redditor)

    assert player.tag_time is not None


@pytest.mark.asyncio
async def test_untag(async_session: AsyncSession, player_repo: IRepository, player: Player):
    tag_time = datetime.now(timezone.utc)
    player.tag_time = tag_time

    async_session.add(player)
    await async_session.commit()
    await async_session.refresh(player)

    assert player.tag_time == tag_time

    service = PlayerService(repo=player_repo)
    mock_redditor = Mock()
    mock_redditor.configure_mock(**test_redditor_one)

    await service.untag(mock_redditor)

    assert player.tag_time is None


@pytest.mark.asyncio
async def test_list_opted_out(
    async_session: AsyncSession, player_repo: IRepository, player: Player
):
    player.opted_out = True

    async_session.add(player)
    await async_session.commit()
    await async_session.refresh(player)

    service = PlayerService(repo=player_repo)
    assert player.username in await service.list_opted_out()


@pytest.mark.asyncio
async def test_set_opted_out_true(
    async_session: AsyncSession, player_repo: IRepository, player: Player
):
    service = PlayerService(repo=player_repo)
    assert player.opted_out is False

    async_session.add(player)
    await async_session.commit()
    await async_session.refresh(player)
    await service.set_opted_out(player.reddit_id, True)

    assert player.opted_out is True
