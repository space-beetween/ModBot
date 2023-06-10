from disnake.ext import commands


GameID = commands.option_enum(
    {
        "Deep Rock Galactic": "@drg",
        "Besiege": "@besiege",
        "Space Enginieers": "@spaceengineers",
        "Insurgency Sandstorm": "@insurgencysandstorm"
    }
)
