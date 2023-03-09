import pytest


@pytest.mark.asyncio
async def test_home_happy_path(async_test_app):
    response = await async_test_app.get("/")
    assert response.status_code == 200
    assert "127.0.0.1" in response.text
