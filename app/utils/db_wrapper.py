from app.utils.logging import log
from typing import Optional

import aiosqlite


class Database:
    """ An embed of the aio-sqlite database class """
    __db: Optional[aiosqlite.Connection] = None

    @classmethod
    async def init(cls):
        cls.__db = await aiosqlite.connect("app/db.sqlite")
        log.success("Connection to the sqlite database is established")


db: Database = Database()
