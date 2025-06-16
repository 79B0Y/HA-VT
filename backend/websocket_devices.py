from fastapi import WebSocket, WebSocketDisconnect, APIRouter
import asyncio
import motor.motor_asyncio
from dotenv import load_dotenv
import os


router = APIRouter()

load_dotenv()
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "virtual_devices")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]


@router.websocket("/ws/devices")
async def websocket_device_updates(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            latest = []
            collections = await db.list_collection_names()
            for name in collections:
                doc = await db[name].find_one(sort=[("timestamp", -1)])
                if doc:
                    latest.append({
                        "did": doc.get("did"),
                        "device_type": doc.get("device_type"),
                        "data": doc.get("data")
                    })
            for item in latest:
                await websocket.send_json(item)
            await asyncio.sleep(3)
    except WebSocketDisconnect:
        print("客户端断开 WebSocket 连接")
    except Exception as e:
        print(f"WebSocket 推送异常: {e}")
