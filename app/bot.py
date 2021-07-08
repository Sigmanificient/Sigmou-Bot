import os
from typing import Any, Callable

import discord
from discord.ext import commands, tasks

import dotenv
from app.timer import time
from app.embeds import Embed
from app.logging import temp_print, warn


class Bot(commands.Bot):

    def __init__(self, prefix: str):
        """Sigmanificient Bot wrapper."""
        super(Bot, self).__init__(
            command_prefix=commands.when_mentioned_or(prefix),
            intents=discord.Intents.default(),
            owner_id=812699388815605791,
            case_insensitive=True
        )

        print(self)
        Embed.load(self)

        self.colour: discord.Colour = discord.Colour(0xCE1A28)
        self._skip_check: Callable[[Any, Any], False] = lambda _x, _y: False
        self.remove_command('help')
        self.load_components()

    def __repr__(self) -> str:
        return '\n'.join(
            (
                r"██████╗  ██████╗     ██████╗  █████╗ ██╗   ██╗███████╗    ██████╗  ██████╗ ████████╗",
                r"╚════██╗██╔═████╗    ██╔══██╗██╔══██╗╚██╗ ██╔╝██╔════╝    ██╔══██╗██╔═══██╗╚══██╔══╝",
                r" █████╔╝██║██╔██║    ██║  ██║███████║ ╚████╔╝ ███████╗    ██████╔╝██║   ██║   ██║",
                r" ╚═══██╗████╔╝██║    ██║  ██║██╔══██║  ╚██╔╝  ╚════██║    ██╔══██╗██║   ██║   ██║",
                r"██████╔╝╚██████╔╝    ██████╔╝██║  ██║   ██║   ███████║    ██████╔╝╚██████╔╝   ██║",
                r"╚═════╝  ╚═════╝     ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝    ╚═════╝  ╚═════╝    ╚═╝"
            )
        )

    def load_components(self):
        for file_name in os.listdir("app/components"):
            if not file_name.endswith("py"):
                continue

            self.load_component(file_name[:-3])

    def load_component(self, component_name: str) -> bool:
        try:
            self.load_extension(f"app.components.{component_name}")

        except commands.ExtensionFailed as error:
            warn(f"Could not load component '{component_name}' due to {error.__cause__}")
            return False

        else:
            temp_print(f"loaded {component_name}")
            return True

    def run(self):
        time("start")
        super().run(self.token)

    @property
    def token(self):
        if self.is_ready():
            return

        return dotenv.dotenv_values(".env").get('TOKEN')

    @tasks.loop(seconds=30)
    async def update_latency(self):
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{self.command_prefix}help | {self.latency * 1000:,.3f} ms"
            )
        )

    async def on_connect(self):
        self.update_latency.start()
