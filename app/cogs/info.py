from os import listdir
from typing import Dict, Tuple, NoReturn

from discord.ext import commands

from app.bot import Bot
from app.timed_ctx import TimedCtx
from app.utils.embeds import Embed
from app.utils.timer import time


class InfoCog(commands.Cog):
    """A simple commands cog template."""

    def __init__(self, client: Bot):
        """Link to bot instance."""
        self.client: Bot = client

        # Preloading file content
        self.files_info: Dict[str, str] = {}

        folders: Tuple[str, ...] = (".", "app", "app/cogs")

        for file, path in {
            _f: path for path in folders for _f in listdir(path) if _f.endswith(".py")
        }.items():
            with open(f"{path}/{file}", encoding="utf-8") as f:
                self.files_info[file] = f.read()

        self.files_info['Total'] = "\n".join(self.files_info.values())

    @commands.command(
        name="ping",
        description="Return Bot Latency",
        brief="Ping command"
    )
    async def ping(self, ctx: TimedCtx) -> None:
        """Return Bot Latency."""
        t: str = time()

        ping_embed = Embed(ctx)(title="Pong !").add_field(
            name="Api latency",
            value=f"> `{self.client.latency * 1000:.3f}` ms"
        )

        message = await ctx.send(embed=ping_embed)

        await message.edit(
            embed=ping_embed.add_field(
                name="Client latency",
                value=f"> `{time(t) * 1000:,.3f}` ms"
            )
        )

    @commands.command(name="code")
    async def get_code_info(self, ctx: TimedCtx) -> None:
        await ctx.send(
            embed=Embed(ctx)(
                title="Code Structure",
                description=f"> This is the whole code structure of {self.client.user.name}!"
            ).add_fields(
                self.files_info,
                map_title=lambda name: f"📝 {name}" if name != "Total" else "📊 Total",
                map_values=lambda file: "`%s` characters\n `%s` lines" % (f"{len(file):,}", len(file.splitlines())),
            )
        )


def setup(client: Bot) -> NoReturn:
    client.add_cog(InfoCog(client))
