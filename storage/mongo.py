import motor.motor_asyncio
import logging
import datetime


class MongoStorage:
    def __init__(self, config):
        self.logger = logging.getLogger("MongoStorage")
        self.mongo_url = config.get("mongo_url", "mongodb://localhost:27017")
        self.db_name = config.get("db_name", "virtual_devices")
        self.client = None
        self.db = None

    async def connect(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(self.mongo_url)
        self.db = self.client[self.db_name]
        self.logger.info(f"连接 MongoDB 数据库: {self.db_name}")

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
