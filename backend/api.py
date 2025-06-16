from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
import os
import motor.motor_asyncio
from dotenv import load_dotenv
from pathlib import Path
from websocket_devices import router as ws_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ws_router)  # ✅ 注册 WebSocket 路由

# 加载环境变量
load_dotenv()
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "virtual_devices")
LOG_PATH = Path(
    os.getenv(
        "LOG_PATH",
        Path(__file__).parent.parent / "core" / "logs" / "simulator.log",
    )
)

client = motor.motor_asyncio.AsyncIOMotorClient(
    MONGO_URL, serverSelectionTimeoutMS=1000
)
db = client[DB_NAME]


@app.get("/api/devices")
async def get_devices():
    result = []
    try:
        collections = await db.list_collection_names()
        for coll in collections:
            async for doc in db[coll].find().sort("timestamp", -1).limit(5):
                result.append({
                    "did": doc.get("did"),
                    "device_type": doc.get("device_type"),
                    "data": doc.get("data")
                })
    except Exception as e:
        print(f"读取设备列表失败: {e}")
    return result


@app.get("/api/logs", response_class=PlainTextResponse)
async def get_logs():
    try:
        return LOG_PATH.read_text(encoding="utf-8")
    except Exception as e:
        return f"无法读取日志文件: {str(e)}"


@app.get("/api/mongo/stats")
async def mongo_stats():
    stats = {"connected": False, "db_name": DB_NAME, "collections": {}}
    try:
        collections = await db.list_collection_names()
        stats["connected"] = True
        for name in collections:
            count = await db[name].count_documents({})
            stats["collections"][name] = count
    except Exception:
        stats["connected"] = False
    return stats
