import os
from datetime import datetime

import discord
from discord.ext import commands

import dotenv
from app.timer import time


class Bot(commands.Bot):

    def __init__(self, prefix):
        super(Bot, self).__init__(
            command_prefix=prefix,
            intents=discord.Intents.default(),
            case_insensitive=True,
        )

        print(self)
        self._skip_check = lambda x, y: False
        self.remove_command('help')
        self.load_extensions()

    def __repr__(self):
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

            print('- loading', filename, end='\r')
            self.load_extension(f"app.components.{filename[:-3]}")
            print('- loaded', filename, end='\r')

    def run(self):
        time("start")
        super().run(self.token)

    @property
    def token(self):
        if self.is_ready():
            return

        return dotenv.dotenv_values(".env").get('TOKEN')

    async def on_connect(self):
        connect_time = time("start", keep=True)
        self.log(f'Logged in as {self.user} after {connect_time:,.3f}s')

    async def on_ready(self):
        ready_time = time("start", keep=True)
        self.log(f'Ready after {ready_time:,.3f}s')

    @staticmethod
    def log(*args):
        print(f"[{datetime.now():%d/%b/%Y:%Hh %Mm %Ss}]", *args)
