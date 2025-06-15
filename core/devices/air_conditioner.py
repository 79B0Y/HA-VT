import asyncio
import random
import logging
import uuid

class AirConditioner:
    def __init__(self, pid, did, mqtt_client, mongo, config):
        self.pid = pid
        self.did = did
        self.name = f"AC_{did}"
        self.logger = logging.getLogger(f"AirConditioner-{did}")
        self.mqtt = mqtt_client
        self.mongo = mongo
        self.update_interval = config.get("update_interval", 10)
        self.static = config.get("static", False)
        self.running = True

        # 状态初始化
        self.state = {
            "pwr": 1,
            "temp": random.randint(22, 26),
            "ac_mode": random.randint(0, 3),
            "ac_mark": random.randint(0, 3),
            "envtemp": random.uniform(20, 30)
        }

    async def run(self):
        await self.publish_discovery()
        await asyncio.sleep(1)
        await self.publish_availability("online")

        while self.running and not self.static:
            self.simulate_status()
            await self.publish_status()
            await self.mongo.insert(self.did, "air_conditioner", self.state)
            await asyncio.sleep(self.update_interval)

    def simulate_status(self):
        # 简单模拟状态变化
        self.state["envtemp"] = round(self.state["envtemp"] + random.uniform(-0.5, 0.5), 1)

    async def publish_discovery(self):
        topic = f"homeassistant/climate/{self.pid}/{self.did}/config"
        payload = {
            "name": self.name,
            "unique_id": self.did,
            "availability_topic": f"home/{self.did}/available",
            "device": {
                "identifiers": [self.did],
                "name": self.name,
                "model": "HVAC",
                "manufacturer": "LinknLink"
            },
            "icon": "mdi:air-conditioner",
            "state_topic": f"home/{self.did}/status",
            "command_topic": f"home/{self.did}/set",
            "temperature_command_topic": f"home/{self.did}/set/temp",
            "fan_mode_command_topic": f"home/{self.did}/set/fan",
            "mode_command_topic": f"home/{self.did}/set/mode",
            "json_attributes_topic": f"home/{self.did}/status",
            "temperature_state_topic": f"home/{self.did}/status",
            "current_temperature_topic": f"home/{self.did}/status",
            "fan_mode_state_topic": f"home/{self.did}/status",
            "mode_state_topic": f"home/{self.did}/status",
            "min_temp": 16,
            "max_temp": 32,
            "temp_step": 1,
            "modes": ["off", "cool", "heat", "dry", "fan_only"],
            "fan_modes": ["auto", "low", "medium", "high"],
            "value_template": "{{ value_json.temp }}",
            "current_temperature_template": "{{ value_json.envtemp }}",
            "fan_mode_value_template": "{{ ['auto', 'low', 'medium', 'high'][value_json.ac_mark] }}",
            "mode_state_template": "{{ ['off','cool','heat','dry','fan_only'][value_json.ac_mode] if value_json.pwr else 'off' }}"
        }
        await self.mqtt.publish(topic, payload, retain=True)

    async def publish_status(self):
        await self.mqtt.publish(f"home/{self.did}/status", self.state)

    async def publish_availability(self, status):
        await self.mqtt.publish(f"home/{self.did}/available", status)
