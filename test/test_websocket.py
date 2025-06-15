import pytest
from fastapi.testclient import TestClient
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "backend"))
from api import app

client = TestClient(app)

def test_websocket_device_stream():
    try:
        with client.websocket_connect("/ws/devices") as websocket:
            assert websocket is not None
    except Exception as e:
        pytest.fail(f"WebSocket 测试失败: {e}")
