import asyncio
import random
import logging
import json


class Sensor:
    def __init__(self, pid, did, mqtt_client, mongo, config):
        self.pid = pid
        self.did = did
        self.name = f"Sensor_{did}"
        self.device_class = config.get("device_class", "temperature")
        self.range = config.get("range", [20, 30])
        self.unit = config.get("unit", "°C")
        self.update_interval = config.get("update_interval", 5)
        self.static = config.get("static", False)
        self.running = True
        self.logger = logging.getLogger(f"Sensor-{did}")
        self.mqtt = mqtt_client
        self.mongo = mongo

        self.value = random.uniform(self.range[0], self.range[1])

    def subscribe_topic(self):
        return f"home/{self.did}/set"

    async def handle_command(self, topic: str, payload: str):
        try:
            data = json.loads(payload)
        except Exception:
            data = payload
        if isinstance(data, dict) and "value" in data:
            self.value = float(data["value"])
        elif (
            isinstance(data, (int, float))
            or str(data).replace(".", "", 1).isdigit()
        ):
            self.value = float(data)

    async def run(self):
        await self.publish_discovery()
        await asyncio.sleep(1)
        await self.publish_availability("online")

        while self.running and not self.static:
            self.simulate_status()
            await self.publish_status()
            await self.mongo.insert(
                self.did,
                self.device_class,
                {"value": self.value},
            )
            await asyncio.sleep(self.update_interval)

    def simulate_status(self):
        delta = random.uniform(-0.3, 0.3)
        self.value = round(
            min(max(self.value + delta, self.range[0]), self.range[1]),
            1,
        )

    async def publish_discovery(self):
        topic = f"homeassistant/sensor/{self.pid}/{self.did}/config"
        payload = {
            "unique_id": self.did,
            "name": self.name,
            "availability_topic": f"home/{self.did}/available",
            "device_class": self.device_class,
            "state_topic": f"home/{self.did}/status",
            "unit_of_measurement": self.unit,
            "value_template": "{{ value_json.value }}",
            "device": {
                "identifiers": [f"did_{self.did}"],
                "name": self.name,
                "model": f"Link&Link {self.device_class.capitalize()} Sensor",
                "manufacturer": "Link&Link"
            }
        }
        await self.mqtt.publish(topic, payload, retain=True)

    async def publish_status(self):
        await self.mqtt.publish(
            f"home/{self.did}/status",
            {"value": self.value},
        )

    async def publish_availability(self, status):
        await self.mqtt.publish(f"home/{self.did}/available", status)
