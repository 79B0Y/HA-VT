import asyncio
import logging
import json
import paho.mqtt.client as mqtt


class MQTTClient:
    def __init__(self, config):
        self.host = config.get("host", "localhost")
        self.port = config.get("port", 1883)
        self.username = config.get("username")
        self.password = config.get("password")
        self.keepalive = config.get("keepalive", 60)

        self.client = mqtt.Client()
        self.logger = logging.getLogger("MQTTClient")

        if self.username:
            self.client.username_pw_set(self.username, self.password)

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

    async def connect(self):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._connect_blocking)

    def _connect_blocking(self):
        self.client.connect(self.host, self.port, self.keepalive)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.logger.info("MQTT 连接成功")
        else:
            self.logger.error(f"MQTT 连接失败，错误码: {rc}")

    def on_disconnect(self, client, userdata, rc):
        self.logger.warning(f"MQTT 断开连接，错误码: {rc}")

    def on_message(self, client, userdata, msg):
        self.logger.debug(f"收到消息: {msg.topic} -> {msg.payload.decode()}")

    def publish(self, topic, payload, retain=False):
        if isinstance(payload, dict):
            payload = json.dumps(payload)
        self.client.publish(topic, payload, retain=retain)

    def subscribe(self, topic):
        self.client.subscribe(topic)
        self.logger.info(f"订阅主题: {topic}")

    def set_message_callback(self, callback):
        self.client.on_message = callback
