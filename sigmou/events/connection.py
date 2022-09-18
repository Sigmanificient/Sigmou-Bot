import logging

from sigmou.utils.db_wrapper import db
from sigmou.utils.timer import time


logger = logging.getLogger(__name__)


async def on_ready(client):
    ready_time: float = time("start", keep=True)
    logger.info(f"Logged In as {client.user.name} after {ready_time:,.3f}s")

    await db.init()
    await client.load_extensions()
