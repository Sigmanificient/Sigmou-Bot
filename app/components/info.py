from discord.ext import commands


class InfoCog(commands.Cog):
    """A simple commands cog template."""

    def __init__(self, client):
        """Link to bot instance."""
        self.client = client

    @commands.command(
        name="ping",
        description="The ping command",
        brief="Ping command"
    )
    async def ping(self, ctx) -> None:
        """A sample command."""
        await ctx.send(f"Pong ! `{self.client.latency * 1000:.3f}` ms")


def setup(client):
    client.add_cog(InfoCog(client))
