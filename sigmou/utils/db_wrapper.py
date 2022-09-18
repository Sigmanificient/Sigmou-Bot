import os
from typing import Optional, Any, Iterable

import aiosqlite
from logging import getLogger


logger = getLogger(__name__)

DB_PATH: str = "sigmou/db/.db"


def log_it(method):
    async def wrapper(self, sql, *args):
        logger.info(f'{method.__name__} with `{sql}` ?= {args}')
        result = await method(self, sql, *args)

        if result:
            logger.info(f'Query returned {result}')
            return result

    return wrapper


class Database:
    """ An embed of the aio-sqlite database class """
    __db: Optional[aiosqlite.Connection] = None

    @classmethod
    async def init(cls) -> bool:
        if not os.path.exists(DB_PATH):
            logger.error("DB not found !")
            return False

        cls.__db = await aiosqlite.connect(DB_PATH)
        logger.info("Connection to the sqlite database is established")
        return True

    @log_it
    async def fetchone(
        self, sql: str, *args: Any, default=None
    ) -> Optional[Any]:
        """Return a row from the database or a default value."""
        async with self.__db.execute(sql, args) as cur:
            async for val in cur:
                return val if len(val) > 1 else val[0]

        return default

    async def fetchall(
        self, sql: str, *args: Any
    ) -> Iterable[Any]:
        async with self.__db.execute(sql, args) as cur:
            return await cur.fetchall()

    @log_it
    async def post(self, sql: str, *args: Any):
        """Execute a query and commit."""
        await self.__db.execute(sql, args)
        await self.__db.commit()


db: Database = Database()
