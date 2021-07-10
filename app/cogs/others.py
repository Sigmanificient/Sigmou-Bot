from typing import Optional, Union

from discord.ext import commands

from app.bot import Bot
from app.timed_ctx import TimedCtx
from app.utils.timer import time


class OtherCog(commands.Cog):
    """Gizmos and Gadget i dont know where to put."""

    def __init__(self, client: Bot):
        """Link to bot instance."""
        self.client: Bot = client

    @commands.command(
        name="timer",
        description="A simple timer commands that start on first call, then give time elapsed.",
        aliases=('time', 't'),
        brief="A simple timer",
    )
    async def timer_command(self, ctx: TimedCtx) -> None:
        """Clear the number of messages asked. If no number is given, clear all message in the channel."""
        t: Union[str, float] = time(ctx.author.id)
        if isinstance(t, float):
            await ctx.send(f"Timer ended: `{t:,.3f}s`")
            return

        await ctx.send("Timer started...")

    @commands.command(
        name="lap",
        description="A command that give the current timer of an user without stopping it.",
        brief="timer lap"
    )
    async def lap_command(self, ctx: TimedCtx) -> None:
        """give the current time of a timer without destroying it."""
        t: Union[bool, float] = time(ctx.author.id, keep=True, create=False)
        await ctx.send(f"`{t:,.3f}s`" if t else "You dont have any timer")


def setup(client: Bot):
    client.add_cog(OtherCog(client))
