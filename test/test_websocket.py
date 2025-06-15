import pytest
import websockets
import asyncio
import json

WS_URL = "ws://localhost:8000/ws/devices"

@pytest.mark.asyncio
async def test_websocket_device_stream():
    try:
        async with websockets.connect(WS_URL) as websocket:
            # 等待一条设备消息
            message = await asyncio.wait_for(websocket.recv(), timeout=5)
            data = json.loads(message)
            assert "did" in data
            assert "device_type" in data
            assert "data" in data
    except Exception as e:
        pytest.fail(f"WebSocket 测试失败: {e}")
