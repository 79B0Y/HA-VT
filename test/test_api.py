import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from api import app  # 确保 FastAPI 实例命名为 app


@pytest.mark.asyncio
async def test_get_devices():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/devices")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_logs():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/logs")
        assert response.status_code == 200
        assert isinstance(response.text, str)


@pytest.mark.asyncio
async def test_get_mongo_stats():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/mongo/stats")
        assert response.status_code == 200
        data = response.json()
        assert "connected" in data
        assert "db_name" in data
