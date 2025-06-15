import yaml
import logging


def load_config(path="config.yaml"):
    logger = logging.getLogger("Config")
    try:
        with open(path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            logger.info(f"成功加载配置文件: {path}")
            return config
    except FileNotFoundError:
        logger.error(f"配置文件未找到: {path}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"解析配置文件失败: {e}")
        raise
