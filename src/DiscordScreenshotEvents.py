import asyncio
import discord
from PIL import ImageGrab
import pyautogui

class DiscordScreenshotEvents():
    def __init__(self, bot, config, screen_x1, screen_y1, screen_x2, screen_y2):
        self.screen_x1 = screen_x1
        self.screen_y1 = screen_y1
        self.screen_x2 = screen_x2
        self.screen_y2 = screen_x2
        self.bot = bot
        self.config = config
        self.emoji_keypress = {}

        for keypress in config.get('KEY_PRESS', 'allowed_keys').split(','):
            emoji = config.get('KEY_MAPPING', keypress)

            if emoji is not "" and emoji is not " ":
                self.emoji_keypress[emoji] = keypress

        self.sent_file = ""
        self.has_reaction = False
        self.channel = discord.Object(self.config.get('DISCORD', 'channel_id'))
        self.chat_log = ""

    async def on_ready(self):
        print('Logged in as ' + self.bot.user.name + ' - ' + self.bot.user.id)

        # set bot status as playing game
        await self.bot.change_presence(game=discord.Game(name=self.config.get('DISCORD', 'game_name')))

        print(self.config.get('DISCORD', 'start_message'))
        print('------')

        while not self.bot.is_closed:
            if not self.has_reaction:
                await self.take_screenshot()
                await self.send_screenshot()

            await asyncio.sleep(
                int(self.config.get('SCREENSHOT', 'max_wait_seconds')))

    async def on_reaction_add(self, reaction, user):
        if user == self.bot.user:
            return

        if reaction.message.id != self.sent_file.id:
            return

        if self.has_reaction:
            return

        self.has_reaction = True

        emoji = self.get_emoji_name(reaction.emoji)
        key = self.get_emoji_keypress(emoji)

        if key != "" and key is not None:
            await self.enter_keypress(key)
            await self.take_screenshot()
            await self.send_screenshot()

    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        self.chat_log += message.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        self.chat_log += " - "
        self.chat_log += message.author.name or message.author.nick or 'unknown'
        self.chat_log += ":\n"
        self.chat_log += message.content
        self.chat_log += "\n"

        for embed in message.embeds:
            self.chat_log += embed.title
            self.chat_log += " (" + embed.url + ")"
            self.chat_log += ": "
            self.chat_log += embed.description

        self.chat_log += "\n"

    async def take_screenshot(self):
        img = ImageGrab.grab(bbox=(
            self.screen_x1,
            self.screen_y1,
            self.screen_x2,
            self.screen_y2
        ))
        img.save(self.config.get('SCREENSHOT', 'file_name'))

    async def send_screenshot(self):
        new_file = await self.bot.send_file(self.channel, self.config.get('SCREENSHOT', 'file_name'))

        for emoji, keypress in self.emoji_keypress.items():
            await self.bot.add_reaction(new_file, emoji)

        if self.sent_file is not "":
            await self.bot.delete_message(self.sent_file)

        self.sent_file = new_file
        self.has_reaction = False

    async def enter_keypress(self, key):
        pyautogui.keyDown(key)
        await asyncio.sleep(float(self.config.get('KEY_PRESS', 'duration')))
        pyautogui.keyUp(key)
        print('Entered key: ' + key)

    def get_emoji_keypress(self, emoji):
        return self.emoji_keypress.get(emoji)

    def get_emoji_name(self, emoji):
        if isinstance(emoji, str):
            return emoji
        else:
            return emoji.name

    def write_chat_log(self):
        file = open(self.config.get('CHAT_LOG', 'file_name'), "w+")
        file.write(self.chat_log)
        file.close()