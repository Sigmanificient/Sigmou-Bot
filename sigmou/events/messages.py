from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .. import Bot
    from discord import Message

from sigmou.utils.db_wrapper import db


async def on_message(client: Bot, message: Message):
    if message.author.id == client.user.id:
        return

    user_point = await db.fetchone(
        "SELECT point FROM users WHERE discord_id = ?",
        message.author.id
    )

    if not user_point:
        await db.post(
            "insert into users(discord_id, point) values (?, 100)",
            message.author.id
        )
    else:
        await db.post(
            "UPDATE users SET point = point + 100 WHERE discord_id = ?",
            message.author.id,
        )
