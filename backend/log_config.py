import logging
import logging.config
import yaml

with open(
    "./log_config.yaml",
    "r",
) as f:
    log_config = yaml.safe_load(f)

logging.config.dictConfig(log_config)
logger = logging.getLogger(__name__)
