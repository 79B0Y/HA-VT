import asyncio
import random
import logging
import uuid
import json

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

    def subscribe_topic(self):
        """返回需要订阅的主题"""
        return f"home/{self.did}/#"

    async def handle_command(self, topic: str, payload: str):
        """处理来自 MQTT 的控制指令"""
        sub = '/'.join(topic.split('/')[2:])  # remove 'home/<did>/'
        try:
            data = json.loads(payload)
        except Exception:
            data = payload

        if sub == 'set':
            if isinstance(data, dict):
                for key in ["pwr", "temp", "ac_mode", "ac_mark"]:
                    if key in data:
                        self.state[key] = int(data[key])
            elif str(data).isdigit():
                self.state["pwr"] = int(data)
        elif sub == 'set/temp':
            if str(data).isdigit():
                self.state["temp"] = int(data)
        elif sub == 'set/fan':
            mapping = {'auto': 0, 'low': 1, 'medium': 2, 'high': 3}
            if isinstance(data, str) and data in mapping:
                self.state["ac_mark"] = mapping[data]
            elif str(data).isdigit():
                self.state["ac_mark"] = int(data)
        elif sub == 'set/mode':
            mapping = {'off': 0, 'cool': 1, 'heat': 2, 'dry': 3, 'fan_only': 4}
            if isinstance(data, str) and data in mapping:
                self.state["ac_mode"] = mapping[data]
                self.state["pwr"] = 0 if mapping[data] == 0 else 1
            elif str(data).isdigit():
                val = int(data)
                self.state["ac_mode"] = val
                self.state["pwr"] = 0 if val == 0 else 1

    async def run(self):
        await self.publish_discovery()
        await asyncio.sleep(1)
        await self.publish_availability("online")
        await self.publish_status()
        await self.mongo.insert(self.did, "air_conditioner", self.state)

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
