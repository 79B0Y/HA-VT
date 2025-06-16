from devices.air_conditioner import AirConditioner
from devices.light import Light
from devices.sensor import Sensor
import itertools


def load_devices_from_config(devices_config, mqtt_client, mongo):
    devices = []
    did_counter = itertools.count(1)

    for dev_type, cfg in devices_config.items():
        pid = cfg.get("pid")

        def make_did():
            return f"{dev_type}_{next(did_counter):04d}"

        # 自动更新设备
        if "auto_update" in cfg:
            auto_cfg = cfg["auto_update"]
            for _ in range(auto_cfg.get("count", 0)):
                did = make_did()
                config = dict(auto_cfg)
                config["static"] = False
                devices.append(
                    create_device(
                        dev_type,
                        pid,
                        did,
                        mqtt_client,
                        mongo,
                        config,
                    )
                )

        # 静态设备
        if "static" in cfg:
            static_cfg = cfg["static"]
            for _ in range(static_cfg.get("count", 0)):
                did = make_did()
                config = dict(static_cfg)
                config["static"] = True
                devices.append(
                    create_device(
                        dev_type,
                        pid,
                        did,
                        mqtt_client,
                        mongo,
                        config,
                    )
                )

    return devices


def create_device(dev_type, pid, did, mqtt_client, mongo, config):
    if dev_type == "air_conditioners":
        return AirConditioner(pid, did, mqtt_client, mongo, config)
    elif dev_type == "lights":
        return Light(pid, did, mqtt_client, mongo, config)
    elif dev_type.endswith("sensors"):
        device_class_map = {
            "temperature_sensors": "temperature",
            "humidity_sensors": "humidity",
            "motion_sensors": "motion",
        }
        config["device_class"] = device_class_map.get(dev_type, "temperature")
        config.setdefault(
            "unit",
            "°C" if config["device_class"] == "temperature" else "%",
        )
        return Sensor(pid, did, mqtt_client, mongo, config)
    else:
        raise ValueError(f"未知的设备类型: {dev_type}")
