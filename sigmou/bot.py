import os
from logging import getLogger
from typing import NoReturn, Optional

import dotenv
from pincer import Client, Intents
from pincer.exceptions import CogError

from sigmou.cogs import cogs
from sigmou.utils.db_wrapper import db
from sigmou.utils.timer import time

logger = getLogger(__name__)


class Bot(Client):
    def __init__(self, prefix: str):
        """Sigmanificient Bot wrapper."""
        token = dotenv.dotenv_values(".env").get("TOKEN")

        if not token:
            raise SystemExit("No token")

        super(Bot, self).__init__(intents=Intents.all(), token=token)

        self.colour = 0xCE1A28
        self.base_prefix: str = prefix

        for cog in cogs:
            self.load_cog(cog)

    @Client.event
    async def on_ready(self):
        ready_time: float = time("start", keep=True)
        logger.info(f"Ready after {ready_time:,.3f}s")
        await db.init()
