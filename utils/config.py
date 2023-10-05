"""Works with the config.yaml file"""
import yaml


class Config:
    """Config"""

    def __init__(self) -> None:
        with open("config.yaml", "r", encoding="UTF=8") as conf:
            self.config = yaml.safe_load(conf)
