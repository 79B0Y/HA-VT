import asyncio
import logging
from pathlib import Path
from mqtt.client import MQTTClient
from storage.mongo import MongoStorage
from devices import load_devices_from_config
from utils.config import load_config


async def main():
    # 初始化日志
    Path("logs").mkdir(parents=True, exist_ok=True)
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

    # 订阅设备指令主题
    device_map = {d.did: d for d in devices}
    for device in devices:
        topic = getattr(device, "subscribe_topic", lambda: None)()
        if topic:
            await mqtt_client.subscribe(topic)

    async def on_msg(topic, payload):
        parts = topic.split('/')
        if len(parts) >= 2:
            did = parts[1]
            dev = device_map.get(did)
            if dev and hasattr(dev, "handle_command"):
                await dev.handle_command(topic, payload)

    mqtt_client.set_callback_handler(on_msg)
    listener_task = asyncio.create_task(mqtt_client.listen())

    # 启动所有设备
    tasks = [device.run() for device in devices]
    tasks.append(listener_task)
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("程序中断退出")

