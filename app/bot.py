import os
from typing import NoReturn, Optional

import dotenv
from pincer import Client, Intents
from pincer.exceptions import CogError

from app.utils.db_wrapper import db
from app.utils.logging import log


class Bot(Client):

    def __init__(self, prefix: str):
        """Sigmanificient Bot wrapper."""
        super(Bot, self).__init__(
            intents=Intents.all(),
            token=self.token
        )

        self.colour = 0xCE1A28
        self.base_prefix: str = prefix
        self.load_components()

    def load_components(self) -> NoReturn:
        for file_name in os.listdir("app/cogs"):
            if not file_name.endswith("py"):
                continue

            self.load_component(file_name[:-3])

    def load_component(self, component_name: str) -> bool:
        try:
            self.load_cog(f"app.cogs.{component_name}")

        except CogError as error:
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
