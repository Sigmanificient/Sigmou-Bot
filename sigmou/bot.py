import os
from logging import getLogger

import dotenv
from discord import Intents
from discord.ext import commands

from sigmou.events import events
from sigmou.injection import client_injection

logger = getLogger(__name__)


class Bot(commands.Bot):
    def __init__(self):
        """Sigmanificient Bot wrapper."""
        super(Bot, self).__init__(intents=Intents.all(), command_prefix=';')
        self.remove_command("help")

    async def load_extensions(self):
        for command in self.tree.get_commands():
            await self.unload_extension(command.name)

        for filename in os.listdir("sigmou/commands"):
            if not filename.endswith(".py") or filename.startswith("_"):
                continue

            print(f"=> sigmou.commands.{filename}")
            await self.load_extension(f"sigmou.commands.{filename[:-3]}")

        print("Syncing tree...")
        await self.tree.sync()

    def run(self, **kwargs):
        token = dotenv.dotenv_values(".env").get("TOKEN")

        if not token:
            logger.error("No token were found in the .env file")
            return

        super().run(token=token, **kwargs)

    def setup_events(self):
        injector = client_injection(self)

        for event in events:
            self.event(injector(event))
