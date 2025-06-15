import asyncio
import logging
import json
from asyncio_mqtt import Client, MqttError


class MQTTClient:
    def __init__(self, config):
        self.host = config.get("host", "localhost")
        self.port = config.get("port", 1883)
        self.username = config.get("username")
        self.password = config.get("password")
        self.keepalive = config.get("keepalive", 60)
        self.logger = logging.getLogger("MQTTClient")
        self._client = Client(
            hostname=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            keepalive=self.keepalive,
        )
        self.reconnect_delay = config.get("reconnect_delay", 3)

    async def connect(self, retries=5):
        for attempt in range(retries):
            try:
                await self._client.connect()
                self.logger.info("MQTT 连接成功")
                return
            except MqttError as e:
                self.logger.warning(f"MQTT 连接失败 (尝试 {attempt+1}/{retries}): {e}")
                await asyncio.sleep(self.reconnect_delay)
        raise RuntimeError("MQTT 重试连接失败")

    async def disconnect(self):
        try:
            await self._client.disconnect()
        except MqttError as e:
            self.logger.warning(f"MQTT 断开失败: {e}")

    async def publish(self, topic: str, payload, retain=False):
        if isinstance(payload, dict):
            payload = json.dumps(payload)
        try:
            await self._client.publish(topic, payload, retain=retain)
        except MqttError as e:
            self.logger.error(f"MQTT 发布失败: {e}")

    async def subscribe(self, topic: str):
        try:
            await self._client.subscribe(topic)
            self.logger.info(f"订阅主题: {topic}")
        except MqttError as e:
            self.logger.error(f"订阅失败: {e}")

    def set_callback_handler(self, callback_coroutine):
        self.callback = callback_coroutine

    async def listen(self):
        try:
            async with self._client.unfiltered_messages() as messages:
                async for msg in messages:
                    try:
                        if hasattr(self, 'callback'):
                            await self.callback(msg.topic, msg.payload.decode())
                    except Exception as e:
                        self.logger.warning(f"消息处理异常: {e}")
        except MqttError as e:
            self.logger.error(f"MQTT 消息监听失败: {e}")
