from disnake.ext import commands


ModioGames = commands.option_enum(
    {
        "Deep Rock Galactic": "@drg",
        "Besiege": "@besiege",
        "Space Enginieers": "@spaceengineers",
        "Insurgency Sandstorm": "@insurgencysandstorm"
    }
)
