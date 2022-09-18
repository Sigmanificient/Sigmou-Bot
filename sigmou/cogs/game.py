from __future__ import annotations

from typing import TYPE_CHECKING

from pincer import command
from pincer.objects import Embed, User

if TYPE_CHECKING:
    from sigmou.bot import Bot

from sigmou.constants import TEST_GUILD_ID
from sigmou.utils.db_wrapper import db


class GameCog:
    """Game commands."""

    def __init__(self, client: Bot):
        """Link to bot instance."""
        self.client: Bot = client

    @command(name="start", guild=TEST_GUILD_ID)
    async def start_command(self, ctx):
        user = await db.fetchone(
            "select true from users where discord_id = ?", ctx.author.user.id
        )

        if user:
            return Embed(title="Error", description="You already have an account !")

        await db.post("insert into users(discord_id) values (?)", ctx.author.user.id)

        return Embed(
            title="Welcome !", description="Your account has just been created !"
        )

    @command(name="daily", cooldown=1, cooldown_scale=84600, guild=TEST_GUILD_ID)
    async def daily_command(self, ctx):
        user = await db.fetchone(
            "select true from users where discord_id = ?", ctx.author.user.id
        )

        if not user:
            return Embed(title="Error", description="You dont have an account !")

        await db.post(
            "UPDATE users SET point = point + 100 WHERE discord_id = ?",
            ctx.author.user.id,
        )

        return "You received your daily points, enjoy !"

    @command(name="profile", guild=TEST_GUILD_ID)
    async def profile_command(self, ctx, user: User = None):
        if user is None:
            user: User = ctx.author.user

        user_exists = await db.fetchone(
            "select true from users where discord_id = ?", user.id
        )

        if not user_exists:
            return Embed(
                title="Error",
                description=(
                    f"{'You' if user.id == ctx.author.user.id else user} "
                    "dont have an account !"
                ),
            )

        point = await db.fetchone(
            "select point from users where discord_id = ?", user.id
        )

        return (
            f"> {'You' if user == ctx.author.user.id else user} "
            f"have `{point or 0}` points !"
        )

    @command(name="leaderboard", guild=TEST_GUILD_ID)
    async def leaderboard(self):
        users = [
            f"`{await self.client.get_user(user)}`: {point:,}"
            for (user, point) in (
                await db.fetchall(
                    "select discord_id, point from users "
                    "order by point desc limit 10"
                )
            )
        ]

        return "\n".join(users)


setup = GameCog
