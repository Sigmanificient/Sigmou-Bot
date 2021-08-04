import asyncio
from typing import Union

from discord.ext import commands

from app.bot import Bot
from app.utils.timed_ctx import TimedCtx
from app.utils.timer import time


class OtherCog(commands.Cog):
    """Gizmos and Gadget i dont know where to put."""

    def __init__(self, client: Bot):
        """Link to bot instance."""
        self.client: Bot = client

    @commands.command(
        name="chrono",
        description=(
            "A simple chronometer commands that start on first call, "
            "then give time elapsed. "
        ),
        aliases=('ch', 'cn'),
        brief="A simple chronometer",
    )
    async def chronometer_command(self, ctx: TimedCtx) -> None:
        """Clear the number of messages asked.
        If no number is given, clear all message in the channel."""
        t: Union[str, float] = time(ctx.author.id)
        if isinstance(t, float):
            await ctx.send(f"Timer ended: `{t:,.3f}s`")
            return

        await ctx.send("Timer started...")

    @commands.command(
        name="lap",
        description=(
            "A command that give the current chronometer time of an user "
            "without stopping it. "
        ),
        brief="chronometer lap"
    )
    async def lap_command(self, ctx: TimedCtx) -> None:
        """give the current time of a timer without destroying it."""
        t: Union[bool, float] = time(ctx.author.id, keep=True, create=False)
        await ctx.send(f"`{t:,.3f}s`" if t else "You dont have any timer")

    @commands.command(
        name="timer",
        description="A command that wait the given time then ping the user.",
        brief="A simple timer command"
    )
    async def timer_command(self, ctx: TimedCtx, seconds: int) -> None:
        """A simple timer that ping you at end"""
        await asyncio.sleep(seconds)
        await ctx.send("> Ended", reference=ctx.message)


def setup(client: Bot):
    client.add_cog(OtherCog(client))
