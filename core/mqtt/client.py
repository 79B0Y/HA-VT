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

    async def connect(self):
        try:
            await self._client.connect()
            self.logger.info("MQTT 连接成功")
        except MqttError as e:
            self.logger.error(f"MQTT 连接失败: {e}")

    async def disconnect(self):
        await self._client.disconnect()

    async def publish(self, topic: str, payload, retain=False):
        if isinstance(payload, dict):
            payload = json.dumps(payload)
        try:
            await self._client.publish(topic, payload, retain=retain)
        except MqttError as e:
            self.logger.error(f"MQTT 发布失败: {e}")

    async def subscribe(self, topic: str):
        await self._client.subscribe(topic)
        self.logger.info(f"订阅主题: {topic}")

    def get_client(self):
        return self._client

    def set_callback_handler(self, callback_coroutine):
        self.callback = callback_coroutine

    async def listen(self):
        async with self._client.unfiltered_messages() as messages:
            async for msg in messages:
                try:
                    if hasattr(self, 'callback'):
                        await self.callback(msg.topic, msg.payload.decode())
                except Exception as e:
                    self.logger.warning(f"MQTT 消息处理异常: {e}")
