from typing import Optional, Union

from disnake import AppCmdInter
from disnake.ext import commands
from modio.game import Game
from modio.mod import Mod
from modio import modioException

from bot import Bot
from message_components.embeds import GameEmbed, ModEmbed


class ModioInfo(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def _get_game(
        self,
        game_id: Union[int, str]
    ) -> Optional[Game]:
        try:
            game = await self.bot.modio_client.async_get_game(
                game_id
            )
        except modioException:
            return None

        return game

    async def _get_mod(
        self,
        game: Game,
        mod_id: Union[int, str]
    ) -> Optional[Mod]:
        try:
            mod = await game.async_get_mod(mod_id)
        except modioException:
            return None

        return mod

    @commands.slash_command(name="game")
    async def game_by_id(
        self,
        inter: AppCmdInter,
        game_id: str
    ) -> None:
        """Provides information about the game"""

        game = await self._get_game(game_id)

        if not game:
            await inter.response.send_message(
                "game not found",
                ephemeral=True
            )
            return

        await inter.response.send_message(embed=GameEmbed(game))

    @commands.slash_command(name="mod")
    async def mod_by_id(
        self,
        inter: AppCmdInter,
        game_id: str,
        mod_id: str
    ) -> None:
        """Provides information about the mod"""

        game = await self._get_game(game_id)

        if not game:
            await inter.response.send_message(
                "game not found",
                ephemeral=True
            )
            return

        mod = await self._get_mod(game, mod_id)

        if not mod:
            await inter.response.send_message(
                "mod not found",
                ephemeral=True
            )
            return

        await inter.response.send_message(embed=ModEmbed(game, mod))


def setup(bot: Bot):
    bot.add_cog(ModioInfo(bot))
