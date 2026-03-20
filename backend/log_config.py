import logging.config
import yaml
from pathlib import Path

log_config_path = Path(__file__).resolve().parent / "log_config.yaml"

with open(log_config_path, "r") as f:
    config = yaml.safe_load(f)

logging.config.dictConfig(config)
logger = logging.getLogger(__name__)
