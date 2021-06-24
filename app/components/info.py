from discord.ext import commands


class InfoCog(commands.Cog):
    """A simple commands cog template."""

    def __init__(self, client):
        """Link to bot instance."""
        self.client = client

    @commands.command(
        name="ping",
        description="Return Bot Latency",
        brief="Ping command"
    )
    async def ping(self, ctx) -> None:
        """Return Bot Latency."""
        await ctx.send(f"Pong ! `{self.client.latency * 1000:.3f}` ms")


def setup(client):
    client.add_cog(InfoCog(client))
