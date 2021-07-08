from discord.ext import commands

from app.timer import time


class ModerationCog(commands.Cog):
    """Admin and Moderator utils command."""

    def __init__(self, client):
        """Link to bot instance."""
        self.client = client

    @commands.command(
        name="purge",
        description="Clear the number of messages asked. If no number is given, clear all message in the channel.",
        aliases=('clear', 'cls'),
        brief="the sample",
    )
    async def sample_command(self, ctx, limit: int = None) -> None:
        """Clear the number of messages asked. If no number is given, clear all message in the channel."""
        await ctx.channel.purge(limit=limit)
        await ctx.send("Purged !")


def setup(client):
    client.add_cog(ModerationCog(client))
