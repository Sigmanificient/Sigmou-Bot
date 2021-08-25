from typing import NoReturn

import discord
from discord.ext import commands

from app.bot import Bot
from app.utils.db_wrapper import db
from app.utils.embeds import Embed
from app.utils.timed_ctx import TimedCtx


class GameCog(commands.Cog):
    """Game commands."""

    def __init__(self, client: Bot):
        """Link to bot instance."""
        self.client: Bot = client
        Embed.load(self.client)

    @commands.command(name="start")
    async def start_command(self, ctx: TimedCtx):
        user = await db.fetchone(
            "select true from users where discord_id = ?", ctx.author.id
        )

        if user:
            await ctx.send(
                embed=Embed(ctx)(
                    title="Error",
                    description="You already have an account !"
                )
            )

            return

        await db.post("insert into users(discord_id) values (?)", ctx.author.id)

        await ctx.send(
            embed=Embed(ctx)(
                title="Welcome !",
                description="Your account has just been created !"
            )
        )

    @commands.command(name="daily")
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily_command(self, ctx: TimedCtx):
        user = await db.fetchone(
            "select true from users where discord_id = ?", ctx.author.id
        )

        if not user:
            await ctx.send(
                embed=Embed(ctx)(
                    title="Error",
                    description="You dont have an account !"
                )
            )

            return

        await db.post(
            "UPDATE users SET point = point + 100 WHERE discord_id = ?",
            ctx.author.id
        )

        await ctx.send("You received your daily points, enjoy !")

    @commands.command(name="profile", aliases=("p", "me"))
    async def profile_command(
            self, ctx: TimedCtx, user: discord.User = None
    ):
        if user is None:
            user = ctx.author

        user_exists = await db.fetchone(
            "select true from users where discord_id = ?", user.id
        )

        if not user_exists:
            await ctx.send(
                embed=Embed(ctx)(
                    title="Error",
                    description=(
                        f"{'You' if user == ctx.author.id else user} "
                        "dont have an account !"
                    )
                )
            )

            return

        point = await db.fetchone(
            "select point from users where discord_id = ?", user.id
        )

        await ctx.send(
            f"> {'You' if user == ctx.author.id else user} "
            f"have `{point or 0}` points !"
        )

    @commands.command(name="leaderboard", aliases=("ldb", "top"))
    async def leaderboard(self, ctx: TimedCtx):
        users = [
            f"`{await self.client.fetch_user(user)}`: {point:,}"
            for (user, point) in (
                await db.fetchall(
                    "select discord_id, point from users "
                    "order by point desc limit 10"
                )
            )
        ]

        await ctx.send('\n'.join(users))


def setup(client: Bot) -> NoReturn:
    client.add_cog(GameCog(client))
