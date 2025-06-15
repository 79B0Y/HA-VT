import pytest
from httpx import AsyncClient, ASGITransport
import sys
from pathlib import Path

# 添加 backend 到导入路径
sys.path.append(str(Path(__file__).resolve().parent.parent / "backend"))
from api import app

@pytest.mark.asyncio
async def test_get_devices():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/devices")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_logs():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/logs")
        assert response.status_code == 200
        assert isinstance(response.text, str)

@pytest.mark.asyncio
async def test_get_mongo_stats():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/mongo/stats")
        assert response.status_code == 200
        data = response.json()
        assert "connected" in data
        assert "db_name" in data
