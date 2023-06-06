from typing import List, Optional
from pathlib import Path

import yaml


class Config:
    bot_token: str
    db_uri: str
    modio_api_key: str
    test_guilds: List[int]

    def __init__(
        self,
        bot_token: str,
        db_uri: str,
        modio_api_key: str,
        test_guilds: Optional[List[int]] = None
    ):
        if test_guilds is None:
            test_guilds = list()

        kwargs = locals().copy()
        kwargs.pop("self")
        self.__dict__.update(kwargs)

    @classmethod
    def from_path(cls, path: Path) -> "Config":
        data = yaml.load(path.read_text("utf-8"), yaml.FullLoader)
        if data is None:
            raise Exception("config is none")

        return cls(**data)


config = Config.from_path(Path("config.yaml"))
