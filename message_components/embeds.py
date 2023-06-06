from typing import List

from disnake import Embed, Color
from modio.game import Game
from modio.mod import Mod

from helpers.formatters import convert_size


class SubscribeEmbed(Embed):
    def __init__(self, title: str, game: Game):
        super().__init__(
            title=title,
            color=Color.brand_green()
        )
        self.set_image(game.logo.original)


class ModEmbed(Embed):
    def __init__(self,
                 game: Game,
                 mod: Mod,
                 ) -> None:
        super().__init__(
            title=mod.name,
            url=f"{game.profile}/m/{mod.name_id}",
            description=mod.summary,
            color=Color.blurple()
        )
        mod_info: List[str] = [
            f"Version: {mod.file.version}",
            f"Size: {convert_size(mod.file.size)}"
        ]

        self.set_author(
            name=game.name,
            url=game.profile,
            icon_url=game.icon.small
        )
        self.set_footer(
            text=mod.submitter.username,
            icon_url=mod.submitter.avatar.original
        )
        self.add_field("Info", "\n".join(mod_info))
        self.add_field("Tags", ", ".join(mod.tags))
        self.set_image(url=mod.logo.original)

        if mod.file.changelog is not None:
            self.add_field(
                "Changelog",
                mod.file.changelog[:1024]
            )


class GameEmbed(Embed):
    def __init__(self, game: Game) -> None:
        super().__init__(
            title=game.name,
            url=game.profile,
            description=game.summary,
            color=Color.blurple()
        )
        self.set_image(game.logo.original)

        if game.stats is None:
            return

        attrs = set(game.stats.__dict__).difference({"date_expires"})

        for attr in attrs:
            self.add_field(
                attr.replace("_", " "),
                getattr(game.stats, attr)
            )
