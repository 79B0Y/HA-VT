import asyncio
import logging
import json
from aiomqtt import Client, MqttError


class MQTTClient:
    def __init__(self, config):
        self.host = config.get("host", "localhost")
        self.port = config.get("port", 1883)
        self.username = config.get("username")
        self.password = config.get("password")
        self.keepalive = config.get("keepalive", 60)
        self.logger = logging.getLogger("MQTTClient")
        self.client = None
        self.context = None
        self.callback = None

    async def connect(self):
        try:
            self.client = Client(
                hostname=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                keepalive=self.keepalive,
            )
            self.context = self.client.__aenter__()
            await self.context
            self.logger.info("MQTT 连接成功")
        except MqttError as e:
            self.logger.error(f"MQTT 连接失败: {e}")

    async def disconnect(self):
        if self.client and self.context:
            await self.client.__aexit__(None, None, None)
            self.logger.info("MQTT 断开连接")

    async def publish(self, topic: str, payload, retain=False):
        if isinstance(payload, dict):
            payload = json.dumps(payload)
        try:
            await self.client.publish(topic, payload, retain=retain)
        except MqttError as e:
            self.logger.error(f"MQTT 发布失败: {e}")

    async def subscribe(self, topic: str):
        try:
            await self.client.subscribe(topic)
            self.logger.info(f"订阅主题: {topic}")
        except MqttError as e:
            self.logger.error(f"订阅失败: {e}")

    def set_callback_handler(self, callback_coroutine):
        self.callback = callback_coroutine

    async def listen(self):
        try:
            if hasattr(self.client, "unfiltered_messages"):
                async with self.client.unfiltered_messages() as messages:
                    async for msg in messages:
                        try:
                            if self.callback:
                                await self.callback(msg.topic, msg.payload.decode())
                        except Exception as e:
                            self.logger.warning(f"MQTT 消息处理异常: {e}")
            else:
                async for msg in self.client.messages:
                    try:
                        if self.callback:
                            await self.callback(msg.topic, msg.payload.decode())
                    except Exception as e:
                        self.logger.warning(f"MQTT 消息处理异常: {e}")
        except MqttError as e:
            self.logger.error(f"监听消息失败: {e}")
