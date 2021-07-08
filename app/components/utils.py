from typing import Optional

from discord.ext import commands
from app.timer import time


class UtilsCog(commands.Cog):
    """Gizmos and Gadget i dont know where to put."""

    def __init__(self, client):
        """Link to bot instance."""
        self.client = client

    @commands.command(
        name="timer",
        description="A simple timer commands that start on first call, then give time elapsed.",
        aliases=('time', 't'),
        brief="A simple timer",
    )
    async def sample_command(self, ctx, name: Optional[str] = None) -> None:
        """Clear the number of messages asked. If no number is given, clear all message in the channel."""
        print(ctx.author.id == self.client.owner_id, name)
        print(self.client.owner_id, ctx.author.id)
        t = time(ctx.author.id if name is None or ctx.author.id != self.client.owner_id else name)
        if isinstance(t, float):
            await ctx.send(f"Timer ended: `{t:,.3f}s`")
            return

        await ctx.send("Timer started...")


def setup(client):
    client.add_cog(UtilsCog(client))