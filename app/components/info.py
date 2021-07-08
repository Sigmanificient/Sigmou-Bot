from os import listdir

from app.embeds import Embed
from discord.ext import commands


class InfoCog(commands.Cog):
    """A simple commands cog template."""

    def __init__(self, client):
        """Link to bot instance."""
        self.client = client

        # Preloading file content
        self.files = {}
        folders = (".", "app", "app/components")
        for file, path in {
            _f: path for path in folders for _f in listdir(path) if _f.endswith(".py")
        }.items():
            with open(f"{path}/{file}", encoding="utf-8") as f:
                self.files[file] = f.read()

        self.files['Total'] = "\n".join(self.files.values())

    @commands.command(
        name="ping",
        description="Return Bot Latency",
        brief="Ping command"
    )
    async def ping(self, ctx) -> None:
        """Return Bot Latency."""
        await ctx.send(f"Pong ! `{self.client.latency * 1000:.3f}` ms")

    @commands.command(name="code")
    async def get_code_info(self, ctx):
        items = "`%s` characters\n `%s` lines"

        code_embed = Embed(
            ctx=ctx,
            title="Code Structure",
            description=f"> This is the whole code structure of {self.client.user.name}!"
        ).add_fields(
            self.files,
            map_title=lambda name: f"📝 {name}" if name != "Total" else "📊 Total",
            map_values=lambda file: items % (f"{len(file):,}", len(file.splitlines())),
        )

        await ctx.send(embed=code_embed)

def setup(client):
    client.add_cog(InfoCog(client))
