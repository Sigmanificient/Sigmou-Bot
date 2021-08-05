from typing import NoReturn
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
    @commands.cooldown(1, 8460, commands.BucketType.user)
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


def setup(client: Bot) -> NoReturn:
    client.add_cog(GameCog(client))
