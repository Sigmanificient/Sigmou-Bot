import dotenv
from discord.ext import commands


class Bot(commands.Bot):

    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)

    def run(self):
        super().run(self.token)

    @property
    def token(self):
        return dotenv.dotenv_values(".env")['TOKEN']

    @staticmethod
    async def on_ready():
        print("Connexion ready")


def main():
    bot = Bot('>')
    bot.run()
