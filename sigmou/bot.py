import os
from logging import getLogger
from typing import Dict

import discord
import dotenv
from discord import Intents
from discord.ext import commands

from sigmou.events import events
from sigmou.injection import client_injection
from sigmou.utils.db_wrapper import db
from sigmou.utils.timer import time

logger = getLogger(__name__)


class Bot(commands.Bot):
    def __init__(self):
        """Sigmanificient Bot wrapper."""
        super(Bot, self).__init__(intents=Intents.all(), command_prefix=';')

        self.__cogs: Dict[str, object] = {}
        self.remove_command("help")

        self.guild = discord.Object(id=1020239029452677180)

    async def load_extensions(self):
        for command in self.tree.get_commands():
            await self.unload_extension(command.name)

        for filename in os.listdir("sigmou/commands"):
            if not filename.endswith(".py") or filename.startswith("_"):
                continue

            print(f"=> sigmou.commands.{filename}")
            await self.load_extension(f"sigmou.commands.{filename[:-3]}")

        await self.tree.sync(guild=self.guild)

    def run(self, **kwargs):
        token = dotenv.dotenv_values(".env").get("TOKEN")

        if not token:
            logger.error("No token were found in the .env file")
            return

        super().run(token=token, **kwargs)
