from app.utils.logging import log
from typing import Optional, Tuple, Any

import aiosqlite


class Database:
    """ An embed of the aio-sqlite database class """
    __db: Optional[aiosqlite.Connection] = None

    @classmethod
    async def init(cls):
        cls.__db = await aiosqlite.connect("app/db.sqlite")
        log.success("Connection to the sqlite database is established")

    async def fetchone(
        self, sql: str, *args: Tuple[Any], default=None
    ) -> Optional[Any]:
        """Return a row from the database or a default value."""
        async with self.__db.execute(sql, args) as cur:
            async for val in cur:
                return val if len(val) > 1 else val[0]

        return default

    async def post(self, sql: str, *args: Tuple[Any]):
        """Execute a query and commit."""
        await self.__db.execute(sql, args)
        await self.__db.commit()


db: Database = Database()
