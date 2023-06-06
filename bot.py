from typing import Final
import asyncio
import logging

from disnake import Intents
from disnake.ext import commands
from modio import Client

from models import setup
from config import config


_log = logging.getLogger(__name__)

INTENTS: Final[Intents] = Intents(guilds=True)


class Bot(commands.InteractionBot):
    def __init__(self):
        super().__init__(
            test_guilds=config.test_guilds,
            intents=INTENTS,
        )
        self.modio_client = Client(api_key=config.modio_api_key)

        self.load_extensions("cogs")

    async def on_disconnect(self):
        _log.info("on_disconnect was called")
        await self.modio_client.close()

    async def on_resumed(self):
        _log.info("on_resumed was called")
        await self.modio_client.start()

    async def on_ready(self):
        _log.info("on_ready was called")
        await self.modio_client.start()


def run():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(setup())
    Bot().run(config.bot_token)
