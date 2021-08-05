import os

from app.utils.logging import log
from typing import Optional, Tuple, Any, Iterable

import aiosqlite

DB_PATH: str = "app/db/.db"


def log_it(method):
    async def wrapper(self, sql, *args):
        log.db(f'{method.__name__} with `{sql}` ?= {args}')
        result = await method(self, sql, *args)

        if result:
            log.db(f'Query returned {result}')
            return result

    return wrapper


class Database:
    """ An embed of the aio-sqlite database class """
    __db: Optional[aiosqlite.Connection] = None

    @classmethod
    async def init(cls) -> bool:
        if not os.path.exists(DB_PATH):
            log.error("DB not found !")
            return False

        cls.__db = await aiosqlite.connect(DB_PATH)
        log.success("Connection to the sqlite database is established")
        return True

    @log_it
    async def fetchone(
        self, sql: str, *args: Tuple[Any], default=None
    ) -> Optional[Any]:
        """Return a row from the database or a default value."""
        async with self.__db.execute(sql, args) as cur:
            async for val in cur:
                return val if len(val) > 1 else val[0]

        return default

    async def fetchall(
        self, sql: str, *args: Tuple[Any]
    ) -> Iterable[Any]:
        async with self.__db.execute(sql, args) as cur:
            return await cur.fetchall()

    @log_it
    async def post(self, sql: str, *args: Tuple[Any]):
        """Execute a query and commit."""
        await self.__db.execute(sql, args)
        await self.__db.commit()


db: Database = Database()
