from typing import Optional

from disnake import AppCmdInter, Guild
from disnake.ext import commands

import models
from bot import Bot
from helpers.structures import GameID
from message_components.embeds import SubscribeEmbed


class ManageGuilds(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def _add_subscription(
        self,
        guild_id: int,
        channel_id: int,
        game_id: str
    ) -> None:
        await models.Subscription.add(
            guild_id=guild_id,
            channel_id=channel_id,
            game_id=game_id
        )
        game = await models.Game.find(
            models.Game.game_id == game_id
        )
        if game is not None:
            return

        await models.Game.add(
            game_id=game_id
        )

    async def _get_subscription(
        self,
        guild: Guild,
        game_id: str
    ) -> Optional[models.Subscription]:
        subscriptions = await models.Subscription.find(
            models.Subscription.guild_id == guild.id,
            models.Subscription.game_id == game_id
        )

        if subscriptions is None:
            return None

        return subscriptions[0]

    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.slash_command()
    async def subscribe(
        self,
        inter: AppCmdInter,
        game_id: GameID
    ) -> None:
        """Subscribe the current channel \
        to mod updates of a game"""

        await inter.response.defer()
        game = self.bot.modio_client.get_game(game_id=game_id)

        subscription = await self._get_subscription(inter.guild, game_id)

        if subscription is not None:
            await inter.edit_original_response(
                "You are already subscribed"
            )
            return

        await self._add_subscription(
            guild_id=inter.guild_id,
            channel_id=inter.channel_id,
            game_id=game_id
        )

        await inter.edit_original_response(
            embed=SubscribeEmbed(
                title=f"You were subscribed to {game.name}",
                game=game
            )
        )

    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.slash_command()
    async def unsubscribe(
        self,
        inter: AppCmdInter,
        game_id: GameID
    ) -> None:
        """Unsubscribe from the current channel"""

        await inter.response.defer()
        game = self.bot.modio_client.get_game(game_id=game_id)

        subscription = await self._get_subscription(
            guild=inter.guild,
            game_id=game_id
        )

        if subscription is None:
            await inter.edit_original_response(
                "You are not subscribed"
            )
            return

        await models.Subscription.delete(
            models.Subscription.id == subscription.id
        )
        await inter.edit_original_response(
            embed=SubscribeEmbed(
                title=f"You have been unsubscribed from {game.name}",
                game=game
            )
        )


def setup(bot: Bot):
    bot.add_cog(ManageGuilds(bot))
