from datetime import datetime

import dotenv
from discord.ext import commands
from app.timer import time


class Bot(commands.Bot):

    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)

    def run(self):
        time("start")

        print(
            '\n'.join((
                r"   ______ ____      ______        __ ",
                r"  /___  // __ \____/ / __/_____  / /_",
                r"   /_  // / / / __  / __  / __ \/ __/",
                r" ___/ // /_/ / /_/ / /_/ / /_/ / /_  ",
                r"/____//\____/\____/_____/\____/\__/  "
            ))
        )

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
