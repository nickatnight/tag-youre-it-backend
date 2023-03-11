import asyncio
from typing import Generator

import pytest
import pytest_asyncio
from asyncpraw import Reddit
from faker import Faker
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from starlette.testclient import TestClient

from src.clients.reddit.inbox import InboxClient
from src.main import app
from src.models.player import Player
from src.models.subreddit import SubReddit
from src.repositories.game import GameRepository
from src.repositories.player import PlayerRepository
from src.repositories.sqlalchemy import BaseSQLAlchemyRepository
from src.repositories.subreddit import SubRedditRepository
from src.services.base import BaseService
from src.services.game import GameService
from src.services.player import PlayerService
from src.services.subreddit import SubRedditService
from src.services.tag import TagService
from tests.unit import test_redditor_one, test_subreddit
from tests.utils import test_engine


fake = Faker()


@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client  # testing happens here


@pytest_asyncio.fixture(scope="module")
async def async_test_app():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="session")
def event_loop(request) -> Generator:  # noqa: indirect usage
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def async_session() -> AsyncSession:
    async_test_session = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)

    async with async_test_session() as s:
        async with test_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

        yield s

    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await test_engine.dispose()


@pytest.fixture
def game_repo(async_session: AsyncSession) -> BaseSQLAlchemyRepository:
    return GameRepository(db=async_session)


@pytest.fixture
def sub_repo(async_session: AsyncSession) -> BaseSQLAlchemyRepository:
    return SubRedditRepository(db=async_session)


@pytest.fixture
def player_repo(async_session: AsyncSession) -> BaseSQLAlchemyRepository:
    return PlayerRepository(db=async_session)


@pytest.fixture
def mock_game_service(game_repo: BaseSQLAlchemyRepository) -> BaseService:
    return GameService(repo=game_repo)


@pytest.fixture
def mock_sub_service(sub_repo: BaseSQLAlchemyRepository) -> BaseService:
    return SubRedditService(repo=sub_repo)


@pytest.fixture
def mock_player_service(player_repo: BaseSQLAlchemyRepository) -> BaseService:
    return PlayerService(repo=player_repo)


@pytest.fixture
def mock_tag_service(
    mock_player_service: BaseService, mock_game_service: BaseService, mock_sub_service: BaseService
) -> TagService:
    return TagService(mock_player_service, mock_game_service, mock_sub_service)


# TODO: add base fields here?
@pytest.fixture
def player() -> Player:
    return Player(
        username=test_redditor_one["name"],
        reddit_id=test_redditor_one["id"],
        icon_img=test_redditor_one["icon_img"],
        is_employee=test_redditor_one["is_employee"],
        created_utc=test_redditor_one["created_utc"],
        verified=False,
        is_suspended=False,
        has_verified_email=True,
    )


@pytest.fixture
def fake_player() -> Player:
    return Player(
        username=fake.first_name().lower(),
        reddit_id=fake.word(),
        icon_img=fake.image_url(),
        is_employee=fake.boolean(),
        created_utc=fake.unix_time(),
        verified=fake.boolean(),
        is_suspended=False,
        has_verified_email=fake.boolean(),
    )


@pytest.fixture
def it_player() -> Player:
    return Player(
        username="iamitplayer",
        reddit_id="testid",
        icon_img=test_redditor_one["icon_img"],
        is_employee=test_redditor_one["is_employee"],
        created_utc=test_redditor_one["created_utc"],
        verified=False,
        is_suspended=False,
        has_verified_email=True,
        is_it=True,
    )


@pytest.fixture
def subreddit() -> SubReddit:
    return SubReddit(
        name=test_subreddit["name"],
        sub_id=test_subreddit["id"],
        display_name=test_subreddit["display_name"],
        created_utc=test_subreddit["created_utc"],
        description=test_subreddit["description"],
        description_html=test_subreddit["description_html"],
        over18=test_subreddit["over18"],
        subscribers=test_subreddit["subscribers"],
        icon_img=test_subreddit["icon_img"],
    )


@pytest.fixture
async def reddit():
    """Mock Reddit instance"""
    async with Reddit(client_id="dummy", client_secret="dummy", user_agent="dummy") as reddit:
        # Unit tests should never issue requests
        reddit._core.request = dummy_request
        yield reddit


async def dummy_request(*args, **kwargs):
    pass


@pytest.fixture
def mock_inbox_client(reddit):
    return InboxClient(reddit=reddit)
