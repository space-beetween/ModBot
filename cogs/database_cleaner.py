from datetime import datetime, timedelta

from disnake.ext import commands, tasks

import models
from bot import Bot


class DatabaseCleaner(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.clear_events.start()

    @tasks.loop(hours=1)
    async def clear_events(self) -> None:
        events = await models.SendedEvent.find()

        for event in events:
            after_adding: timedelta = datetime.now() - event.data_added

            if after_adding.days > 5:
                await models.SendedEvent.delete(
                    models.SendedEvent.id == event.id
                )


def setup(bot: Bot) -> None:
    bot.add_cog(DatabaseCleaner(bot))
