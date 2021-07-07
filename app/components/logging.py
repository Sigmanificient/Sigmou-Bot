from app.timer import time
from discord.ext import commands


class LoggingCog(commands.Cog):
    """A simple commands cog template."""

    def __init__(self, client):
        """Link to bot instance."""
        self.client = client

    @commands.Cog.listener()
    async def on_connect(self):
        connect_time: float = time("start", keep=True)
        self.client.log(f'Logged in as {self.client.user} after {connect_time:,.3f}s')

    @commands.Cog.listener()
    async def on_ready(self):
        ready_time: float = time("start", keep=True)
        self.client.log(f'Ready after {ready_time:,.3f}s')

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        self.client.log(f"Successfully completed {ctx.command.name} by {ctx.author}")


def setup(client):
    client.add_cog(LoggingCog(client))
