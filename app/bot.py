from datetime import datetime

import discord
from discord.ext import commands

import dotenv
from app.timer import time


class Bot(commands.Bot):

    def __init__(self, command_prefix):
        print(self)

        super(Bot, self).__init__(
            command_prefix=command_prefix,
            intents=discord.Intents.default(),
            case_insensitive=True,
        )

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

    def run(self):
        time("start")
        super().run(self.token)

    @property
    def token(self):
        if self.is_ready():
            return

        return dotenv.dotenv_values(".env")['TOKEN']

    async def on_connect(self):
        connect_time = time("start", keep=True)
        self.log(f'Logged in as {self.user} after {connect_time:,.3f}s')

    async def on_ready(self):
        ready_time = time("start", keep=True)
        self.log(f'Ready after {ready_time:,.3f}s')

    @staticmethod
    def log(*args):
        print(f"[{datetime.now():%d/%b/%Y:%Hh %Mm %Ss}]", *args)


def main():
    bot = Bot('>')
    bot.run()
