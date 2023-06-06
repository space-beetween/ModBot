# ModBot
ModBot is a bot for viewing information from https://mod.io/

You can add it via this [link](https://discord.com/oauth2/authorize?client_id=1115217216963608608&permissions=274877958144&scope=bot%20applications.commands)

## Commands
* `/game <ID>` - Returns information about the game
* `/mod <Game_ID> <Mod_ID>`- Returns information about the game's mod
* `/subscribe <Game_ID>` - Subscribes your guild to mod updates
* `/unsubscribe <Game_ID>` - Unsubscribes your guild from mod updates

## Running localy
### Requirements
* `python 3.8 or higher`
### Installing
Clone this repository and install the packages from `requirements.txt`

After that, modify the `config.yaml` file
```yaml
bot_token: "your discord bot token"
modio_api_key: "your modio api key"
db_uri: "dialect+async_driver://username:password@host:port/database"
test_guilds: [your bot test guilds ids]
```
And run the bot
```
python3 main.py
```
