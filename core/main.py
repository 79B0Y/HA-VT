import asyncio
import logging
from mqtt.client import MQTTClient
from storage.mongo import MongoStorage
from devices import load_devices_from_config
from utils.config import load_config


async def main():
    # 初始化日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler("logs/simulator.log"),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)

    # 加载配置
    config = load_config("config.yaml")
    logger.info("配置加载完成")

    # 初始化数据库
    mongo = MongoStorage(config["database"])
    await mongo.connect()
    logger.info("MongoDB 连接成功")

    # 初始化 MQTT 客户端
    mqtt_client = MQTTClient(config["mqtt"])
    await mqtt_client.connect()
    logger.info("MQTT 连接成功")

    # 初始化并运行所有设备
    devices = load_devices_from_config(config["devices"], mqtt_client, mongo)
    logger.info(f"加载设备数量: {len(devices)}")

    # 启动所有设备
    tasks = [device.run() for device in devices]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("程序中断退出")

