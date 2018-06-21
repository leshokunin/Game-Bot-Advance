# Game Bot Advance - A Discord Bot for "Twitch Plays" types of games

On a Windows machine:
- Select a screen area for the bot to capture
- The bot posts these screenshots to a Discord channel every few seconds
- Users can control the inputs on the PC, using Discord reactions (emoji)

## Getting Started

## To simply use the bot:
Open config.ini: (make sure you save in UTF8!)
1) Configure the bot token:
bot_token - https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token

2) Configure the channel ID:
channel_id - https://github.com/Chikachi/DiscordIntegration/wiki/How-to-get-a-token-and-channel-ID-for-Discord

(optional):
max_wait_seconds: change how long to wait between screenshots

3) Simply run Game Bot Advance.exe, capture a screen area, and voila!


## Using the source:

Install the package dependencies by running the following command:
pip3 install -r requirements.txt

Requirements:
- Asyncio
- Configparser
- Discord
- Pillow
- Pyautogui
- PyQt5

## Default Emoji Names
Every single keyboard key can be rebound to an emoji. You can find those in config.ini.

The current names found in the config file for the emojis can be shown on discord by typing the following:
up = :arrow_up:
down = :arrow_down:
left = :arrow_left:
right = :arrow_right:

https://apps.timwhitlock.info/unicode/inspect?s=%E2%AC%87