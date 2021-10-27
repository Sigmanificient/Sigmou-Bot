import os
from typing import NoReturn, Optional

import dotenv
from discord import Activity, ActivityType, Colour
from discord.ext import commands, tasks
from discord_components import DiscordComponents

from app.utils.db_wrapper import db
from app.utils.logging import log
from app.utils.timer import time
from pincer import Client, Intents


class Bot(Client):

    def __init__(self, prefix: str):
        """Sigmanificient Bot wrapper."""
        super(Bot, self).__init__(
            # case_insensitive=True,
            # command_prefix=commands.when_mentioned_or(prefix),
            # owner_ids=(812699388815605791, 856491941184536597),
            intents=Intents.all(),
            token=self.token
        )

        # self._skip_check = lambda x, y: False
        self.colour: Colour = Colour(0xCE1A28)
        self.base_prefix: str = prefix

        # removing default help command for overriding
        # self.remove_command('help')
        self.load_components()

    def load_components(self) -> NoReturn:
        for file_name in os.listdir("app/cogs"):
            if not file_name.endswith("py"):
                continue

            self.load_component(file_name[:-3])

    def load_component(self, component_name: str) -> bool:
        try:
            self.load_cog(f"app.cogs.{component_name}")

        except commands.ExtensionFailed as error:
            log.error(
                f"Could not load component '{component_name}' "
                f"due to {error.__cause__}"
            )
            return False

        else:
            log.success(f"loaded {component_name}")
            return True

    @property
    def token(self) -> Optional[str]:
        return dotenv.dotenv_values(".env").get('TOKEN')

    @Client.event
    async def on_ready(self):
        await db.init()
