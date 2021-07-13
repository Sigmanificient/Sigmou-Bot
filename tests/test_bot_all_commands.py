import asyncio
import os
import random
import string
import sys
from typing import Optional, List

import discord

import app.bot

TEST_SERVER_ID: int = 857336281583059005
TEST_CHANNEL_ID: int = 864244358517358612

commands_to_test: List[str] = [
]


class Bot(app.bot.Bot):

    def __init__(self):
        test_prefix = ''.join(random.choice(string.ascii_letters) for _ in range(16)) + '_'

        super().__init__(test_prefix)
        self.command_prefix = test_prefix
        self._skip_check = lambda x, y: False

        self.test_channel: Optional[discord.TextChannel] = None

    async def on_ready(self):
        test_server: Optional[discord.Guild] = self.get_guild(TEST_SERVER_ID)

        if test_server is None:
            await self.close()
            raise ValueError("Invalid server ID.")

        self.test_channel = test_server.get_channel(TEST_CHANNEL_ID)

        if self.test_channel is None:
            self.test_channel = await test_server.create_text_channel(f"auto-test {self.user}")

        for command in commands_to_test:
            await self.test_channel.send(f"{self.command_prefix}{command}")

        await asyncio.sleep(10)
        await self.test_channel.send("**Automated test complete.**")

    async def on_message(self, message):
        if message.author != self.user:
            return

        await self.process_commands(message)


def main():
    os.chdir('..')
    bot = Bot()
    bot.run()


if __name__ == '__main__':
    main()
