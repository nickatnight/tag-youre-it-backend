from unittest.mock import AsyncMock

import pytest


@pytest.mark.asyncio
async def test_subreddits_empty_set(async_test_app, mocker):
    patch_repo = mocker.patch("src.api.v1.subreddit.SubRedditRepository.all", AsyncMock())
    patch_repo.return_value = []

    response = await async_test_app.get("/v1/subreddits")
    assert response.status_code == 200
    assert response.json() == {"message": "Data fetched successfully", "meta": {}, "data": []}
