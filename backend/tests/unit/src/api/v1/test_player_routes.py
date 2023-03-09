from unittest.mock import AsyncMock

import pytest


@pytest.mark.asyncio
async def test_players_empty_set(async_test_app, mocker):
    patch_repo = mocker.patch("src.api.v1.player.PlayerRepository.all", AsyncMock())
    patch_repo.return_value = []

    response = await async_test_app.get("/v1/players")
    assert response.status_code == 200
    assert response.json() == {"message": "Data fetched successfully", "meta": {}, "data": []}
