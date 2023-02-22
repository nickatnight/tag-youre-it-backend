import pytest
from mock import Mock

from src.models.subreddit import SubReddit
from src.repositories.subreddit import SubRedditRepository
from src.services.subreddit import SubRedditService
from tests.unit import test_subreddit


@pytest.mark.asyncio
async def test_get_or_create_when_object_doesnt_exist(sub_repo: SubRedditRepository):
    repo = SubRedditService(repo=sub_repo)
    mock_subreddit = Mock()
    mock_subreddit.configure_mock(**test_subreddit)
    instance = await repo.get_or_create(mock_subreddit)

    assert type(instance) == SubReddit
    assert instance.name == test_subreddit["name"]
