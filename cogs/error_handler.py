from typing import Final

from disnake import AppCmdInter, Event
from disnake.ext import commands

from bot import Bot


EVENT: Final[str] = Event.slash_command_error


class ErrorHandler(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.Cog.listener(EVENT)
    async def on_error(
        self,
        inter: AppCmdInter,
        error: commands.CommandError
    ) -> None:
        if isinstance(error, commands.MissingPermissions):
            missing_perms = "\n".join(error.missing_permissions)
            await inter.send(
                f"Missing permissions:\n{missing_perms}",
                ephemeral=True
            )
            return

        raise error


def setup(bot: Bot):
    bot.add_cog(ErrorHandler(bot))
