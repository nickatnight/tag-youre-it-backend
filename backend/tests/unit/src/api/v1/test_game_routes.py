from unittest.mock import AsyncMock

import pytest


@pytest.mark.asyncio
async def test_games_empty_set(async_test_app, mocker):
    patch_repo = mocker.patch("src.api.v1.game.GameRepository.all", AsyncMock())
    patch_repo.return_value = []

    response = await async_test_app.get("/v1/games")
    assert response.status_code == 200
    assert response.json() == {"message": "Data fetched successfully", "meta": {}, "data": []}
