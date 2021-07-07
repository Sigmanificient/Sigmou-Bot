from discord.ext import commands


class LoggingCog(commands.Cog):
    """A simple commands cog template."""

    def __init__(self, client):
        """Link to bot instance."""
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.send(f"**Error report for command `{ctx.command}`**")
        await ctx.send(f"```{error}```")
        await ctx.send(f"```{error!r}```")


def setup(client):
    client.add_cog(LoggingCog(client))
