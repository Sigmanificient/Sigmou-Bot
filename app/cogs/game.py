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


def setup(client: Bot) -> NoReturn:
    client.add_cog(GameCog(client))
