import asyncio
from typing import Union

from pincer import command

from app.bot import Bot
from app.constants import TEST_GUILD_ID
from app.utils.timer import time


class OtherCog:
    """Gizmos and Gadget i dont know where to put."""

    def __init__(self, client: Bot):
        """Link to bot instance."""
        self.client: Bot = client

    @command(
        name="chronometer",
        description=(
                "A simple chronometer commands that start on first call, "
                "then give time elapsed. "
        ),
        guild=TEST_GUILD_ID
    )
    async def chronometer_command(self, ctx) -> str:
        """Clear the number of messages asked.
        If no number is given, clear all message in the channel."""

        t: Union[str, float] = time(ctx.author.user.id)

        if isinstance(t, float):
            return f"Timer ended: `{t:,.3f}s`"

        return "Timer started..."

    @command(
        name="lap",
        description=(
                "A command that give the current chronometer time of an user "
                "without stopping it. "
        ),
        guild=TEST_GUILD_ID
    )
    async def lap_command(self, ctx) -> str:
        """give the current time of a timer without destroying it."""
        t: Union[bool, float] = time(ctx.author.user.id, keep=True, create=False)
        return f"`{t:,.3f}s`" if t else "You dont have any timer"

    @command(
        name="timer",
        description="A command that wait the given time then ping the user.",
        guild=TEST_GUILD_ID
    )
    async def timer_command(self, seconds: int) -> str:
        """A simple timer that ping you at end"""
        yield "started..."
        await asyncio.sleep(seconds)
        yield "> Ended"


setup = OtherCog
