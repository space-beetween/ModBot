import logging
from typing import List, Dict, Final

from disnake import NotFound, Forbidden
from disnake.ext import commands, tasks
from modio import Filter, EventType, modioException
from modio.game import Game
from modio.entities import Event
from modio.mod import Mod

import models
from message_components.embeds import ModEmbed
from bot import Bot


_log = logging.getLogger(__name__)

MESSAGE_CONTENTS: Final[Dict[str, str]] = {
    EventType.available: "A new mod available :tada:",
    EventType.file_changed: "A mod has been updated"
}


class ModioEvents(commands.Cog):
    def __init__(self, bot: "Bot") -> None:
        self.bot = bot
        self.mod_event_handler.start()

    async def _get_mod_events(self, game: Game) -> List[Event]:
        events = []

        # bruh
        game.id = f"@{game.name_id}"

        filter = Filter()
        filter.limit(1)

        for event_type in (EventType.available, EventType.file_changed):
            filter.equals(event_type=event_type)
            try:
                returned_events = await game.async_get_mod_events(
                    filters=filter
                )
            except KeyError:
                returned_events = None

            if returned_events is None:
                event = None
            else:
                event = returned_events.results[0]

            events.append(event)

        return events

    async def _send_mod(
        self,
        game: Game,
        msg_content: str,
        mod: Mod
    ) -> None:
        subscriptions = await models.Subscription.find(
                    models.Subscription.game_id == f"@{game.name_id}"
                )

        for subscription in subscriptions:
            try:
                channel = await self.bot.fetch_channel(
                            subscription.channel_id
                        )
            except NotFound:
                await models.Subscription.delete(
                    models.Subscription.channel_id == subscription.channel_id
                )
                continue

            try:
                await channel.send(
                            content=msg_content,
                            embed=ModEmbed(game, mod)
                        )
            except Forbidden:
                _log.warn(
                    f"failed to send event (ch id: {subscription.channel_id})"
                )

    @tasks.loop(minutes=1)
    async def mod_event_handler(self):
        _log.info("mod_event_handler was called")
        games = await models.Game.find()

        for game in games:
            game = await self.bot.modio_client.async_get_game(
                game.game_id
            )

            events = await self._get_mod_events(
                game
            )

            for event in events:
                if event is None:
                    continue

                try:
                    msg_content = MESSAGE_CONTENTS[event.type]
                except KeyError:
                    continue

                try:
                    mod = await game.async_get_mod(
                        event.mod
                    )
                except modioException:
                    _log.info(f"failed to get mod with id {event.mod}")
                    continue

                sended_event = await models.SendedEvent.find(
                    (models.SendedEvent.mod_file_id == mod.file.id) |
                    (models.SendedEvent.event_id == event.id)
                )
                if len(sended_event) != 0:
                    continue

                await self._send_mod(game, msg_content, mod)

                await models.SendedEvent.add(
                    event_id=event.id,
                    mod_file_id=mod.file.id,
                    game_id=f"@{game.name_id}"
                )

    @mod_event_handler.before_loop
    async def before_event_task(self):
        await self.bot.wait_until_ready()


def setup(bot: Bot):
    bot.add_cog(ModioEvents(bot))
