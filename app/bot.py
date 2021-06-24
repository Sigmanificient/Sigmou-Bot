import os
from typing import Any, Callable

import discord
from discord.ext import commands, tasks

import dotenv
from app.timer import time
from app.logging import Logger


class Bot(commands.Bot):

    def __init__(self, prefix: str):
        super(Bot, self).__init__(
            command_prefix=prefix,
            intents=discord.Intents.default(),
            case_insensitive=True,
        )

        print(self)
        self.log: Logger = Logger()
        self._skip_check: Callable[[Any, Any], False] = lambda _x, _y: False
        self.remove_command('help')
        self.load_extensions()

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

    def load_extensions(self):
        for filename in os.listdir("app/components"):
            if not filename.endswith("py"):
                continue

            component_name: str = filename[:-3]

            self.log(f"loading {component_name}", temp=True)
            self.load_extension(f"app.components.{component_name}")
            self.log(f"loaded {component_name}", temp=True)

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
        connect_time: float = time("start", keep=True)
        self.log(f'Logged in as {self.user} after {connect_time:,.3f}s')
        self.update_latency.start()

    async def on_ready(self):
        ready_time: float = time("start", keep=True)
        self.log(f'Ready after {ready_time:,.3f}s')

    async def on_command_completion(self, ctx):
        print(dir(ctx.command), dir(ctx), ctx.command.clean_params)
