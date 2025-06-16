import motor.motor_asyncio
import logging
import datetime
import asyncio


class MongoStorage:
    def __init__(self, config):
        self.logger = logging.getLogger("MongoStorage")
        self.mongo_url = config.get("mongo_url", "mongodb://localhost:27017")
        self.db_name = config.get("db_name", "virtual_devices")
        self.client = None
        self.db = None

    async def connect(self, retries=5, delay=3):
        for attempt in range(retries):
            try:
                self.client = motor.motor_asyncio.AsyncIOMotorClient(
                    self.mongo_url
                )
                await self.client.server_info()
                self.db = self.client[self.db_name]
                self.logger.info(f"连接 MongoDB 成功: {self.db_name}")
                return
            except Exception as e:
                self.logger.warning(
                    f"MongoDB 连接失败 (尝试 {attempt + 1}/{retries}): {e}"
                )
                await asyncio.sleep(delay)
        raise RuntimeError("无法连接 MongoDB")

    async def insert(self, did, device_type, data):
        try:
            collection = self.db[device_type]
            doc = {
                "did": did,
                "device_type": device_type,
                "timestamp": datetime.datetime.utcnow(),
                "data": data
            }
            await collection.insert_one(doc)
            self.logger.debug(f"写入 MongoDB: {did} => {data}")
        except Exception as e:
            self.logger.error(f"写入 MongoDB 失败: {e}")

    async def ensure_ttl_indexes(self, ttl_seconds: int = 86400):
        try:
            collections = await self.db.list_collection_names()
            for name in collections:
                await self.db[name].create_index(
                    "timestamp",
                    expireAfterSeconds=ttl_seconds,
                    name="timestamp_ttl"
                )
                self.logger.info(
                    f"设置 TTL 索引: {name}.timestamp ({ttl_seconds}秒)"
                )
        except Exception as e:
            self.logger.error(f"设置 TTL 索引失败: {e}")
