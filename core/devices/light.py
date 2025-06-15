import asyncio
import random
import logging


class Light:
    def __init__(self, pid, did, mqtt_client, mongo, config):
        self.pid = pid
        self.did = did
        self.name = f"Light_{did}"
        self.logger = logging.getLogger(f"Light-{did}")
        self.mqtt = mqtt_client
        self.mongo = mongo
        self.update_interval = config.get("update_interval", 5)
        self.static = config.get("static", False)
        self.running = True

        self.state = {
            "pwr": 1,
            "brightness": random.randint(20, 100),
            "colortemp": random.randint(2500, 6500),
            "red": random.randint(0, 255),
            "green": random.randint(0, 255),
            "blue": random.randint(0, 255),
            "bulb_colormode": random.randint(0, 1)  # 0=RGB, 1=色温
        }

    async def run(self):
        self.publish_discovery()
        await asyncio.sleep(1)
        self.publish_availability("online")

        while self.running and not self.static:
            self.simulate_status()
            self.publish_status()
            await self.mongo.insert(self.did, "light", self.state)
            await asyncio.sleep(self.update_interval)

    def simulate_status(self):
        # 随机波动亮度、色温或颜色
        if self.state["bulb_colormode"] == 0:
            self.state["red"] = max(0, min(255, self.state["red"] + random.randint(-10, 10)))
            self.state["green"] = max(0, min(255, self.state["green"] + random.randint(-10, 10)))
            self.state["blue"] = max(0, min(255, self.state["blue"] + random.randint(-10, 10)))
        else:
            self.state["colortemp"] = max(2500, min(6500, self.state["colortemp"] + random.randint(-200, 200)))
        self.state["brightness"] = max(0, min(100, self.state["brightness"] + random.randint(-5, 5)))

    def publish_discovery(self):
        topic = f"homeassistant/light/{self.pid}/{self.did}/config"
        payload = {
            "unique_id": self.did,
            "name": self.name,
            "availability_topic": f"home/{self.did}/available",
            "state_topic": f"home/{self.did}/status",
            "command_topic": f"home/{self.did}/switch",
            "state_value_template": "{{ value_json.pwr }}",
            "payload_on": 1,
            "payload_off": 0,

            "brightness": True,
            "brightness_scale": 100,
            "brightness_state_topic": f"home/{self.did}/status",
            "brightness_command_topic": f"home/{self.did}/brightness/set",
            "brightness_value_template": "{{ value_json.brightness }}",
            "brightness_command_template": "{\"brightness\": {{value}},\"bulb_colormode\":1}",

            "color_mode_state_topic": f"home/{self.did}/status",
            "color_mode_value_template": "{{ 'rgb' if value_json.bulb_colormode == 0 else 'color_temp' }}",

            "color_temp_value_template": "{{ (1000000 / value_json.colortemp) | int }}",
            "color_temp_state_topic": f"home/{self.did}/status",
            "color_temp_command_template": "{\"colortemp\": {{(1000000 / value) | int}},\"bulb_colormode\":1}",
            "color_temp_command_topic": f"home/{self.did}/colortemp/set",

            "rgb_state_topic": f"home/{self.did}/status",
            "rgb_command_topic": f"home/{self.did}/rgb/set",
            "rgb_command_template": "{\"red\":{{red}},\"green\":{{green}},\"blue\":{{blue}},\"bulb_colormode\":0}",
            "rgb_value_template": "{{ value_json.red }},{{ value_json.green }},{{ value_json.blue }}",

            "device": {
                "identifiers": [f"did_{self.did}"],
                "name": self.name,
                "model": "Link&Link Light",
                "manufacturer": "Link&Link"
            }
        }
    await self.mqtt.publish(topic, payload, retain=True)

    def publish_status(self):
    await self.mqtt.publish(f"home/{self.did}/status", self.state)

    def publish_availability(self, status):
    await self.mqtt.publish(f"home/{self.did}/available", status)
