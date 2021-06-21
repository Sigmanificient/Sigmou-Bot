from datetime import datetime
import time

import dotenv
from discord.ext import commands


class Bot(commands.Bot):

    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)

    @property
    def token(self):
        return dotenv.dotenv_values(".env")['TOKEN']

    async def on_connect(self):
        self.log(f'Logged in as {self.user} after {time.perf_counter():,.3f}s')

    async def on_ready(self):
        self.log(f'Ready after {time.perf_counter():,.3f}s')

    @staticmethod
    def log(*args):
        print(f"[{datetime.now():%d/%b/%Y:%Hh %Mm %Ss}]", *args)


def main():
    bot = Bot('>')
    bot.run(bot.token)
