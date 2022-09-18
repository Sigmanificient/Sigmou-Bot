import logging
from time import perf_counter

from sigmou.utils.db_wrapper import db


logger = logging.getLogger(__name__)


async def on_ready(client):
    ready_time = perf_counter() - client.init_marker
    logger.info(f"Logged In as {client.user.name} after {ready_time:,.3f}s")

    await db.init()
    await client.load_command_groups()
