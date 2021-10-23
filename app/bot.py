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

    def unload_component(self, component_name: str) -> bool:
        try:
            self.unload_extension(f"app.cogs.{component_name}")

        except commands.ExtensionFailed as error:
            log.error(
                f"Could not unload component '{component_name}' "
                f"due to {error.__cause__}"
            )
            return False

        else:
            log.success(f"unloaded {component_name}")
            return True

    # def run(self) -> NoReturn:
    #     time("start")
    #     super().run(self.token)

    @property
    def token(self) -> Optional[str]:
        # if self.is_ready():
        #    return

        return dotenv.dotenv_values(".env").get('TOKEN')

    @tasks.loop(seconds=30)
    async def update_latency(self) -> None:
        await self.change_presence(
            activity=Activity(
                type=ActivityType.watching,
                name=f"{self.base_prefix}help | {self.latency * 1000:,.3f} ms"
            )
        )

    async def on_connect(self) -> NoReturn:
        self.update_latency.start()
        db_conn = await db.init()

        if not db_conn:
            log.warn("unloading db connected cogs.")
            self.unload_component("game")

    async def on_ready(self):
        DiscordComponents(self)

    async def process_commands(self, message) -> NoReturn:
        ctx = await self.get_context(message)
        ctx.time = time()

        await self.invoke(ctx)
