import inspect
from os import listdir
from typing import Dict, Tuple, NoReturn, List

import psutil
from discord.ext import commands
from pincer import command
from pincer.objects import Embed as p_Embed

from app.bot import Bot
from app.constants import TEST_GUILD_ID
from app.utils.timed_ctx import TimedCtx
from app.utils.embeds import Embed
from app.utils.timer import time


class InfoCog(commands.Cog):
    """A simple commands cog template."""

    def __init__(self, client: Bot):
        """Link to bot instance."""
        self.client: Bot = client
        Embed.load(self.client)

        # Preloading file content
        self.files_info: Dict[str, str] = {}

        folders: Tuple[str, ...] = (".", "app", "app/cogs")

        for file, path in {
            _f: path for path in folders
            for _f in listdir(path) if _f.endswith(".py")
        }.items():
            with open(f"{path}/{file}", encoding="utf-8") as f:
                self.files_info[file] = f.read()

        self.files_info['Total'] = "\n".join(self.files_info.values())

    @commands.command(
        name="ping",
        description="Return Bot Latency",
        brief="Ping command"
    )
    async def ping_command(self, ctx: TimedCtx) -> None:
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
    async def code_command(self, ctx: TimedCtx) -> None:
        await ctx.send(
            embed=Embed(ctx)(
                title="Code Structure",
                description=(
                    "> This is the whole code structure of "
                    f"{self.client.user.name}!"
                )
            ).add_fields(
                self.files_info,
                map_title=lambda name: (
                    f"📝 {name}" if name != "Total" else "📊 Total"
                ),
                map_values=lambda file: (
                    f"`{len(file)}` characters"
                    f"\n `{len(file.splitlines())}` lines"
                ),
            )
        )

    @command(
        name="panel",
        guild=TEST_GUILD_ID
    )
    async def panel_stats(self) -> p_Embed:
        mb: int = 1024 ** 2

        vm = psutil.virtual_memory()
        cpu_freq = psutil.cpu_freq()
        cpu_percent = psutil.cpu_percent()
        disk = psutil.disk_usage('.')

        stats = {
            'ram': (
                100 * (vm.used / vm.total),
                f'{(vm.total / mb) / 1000:,.3f}',
                'Gb'
            ),
            'cpu': (
                cpu_percent,
                f"{cpu_freq.current / 1000:.1f}`/`{cpu_freq.max / 1000:.1f}",
                'Ghz'
            ),
            'disk': (
                100 * (disk.used / disk.total),
                f'{disk.total / mb:,.0f}', 'Mb'
            )
        }

        return p_Embed(
            title="Server Report",
            description="The bot is hosted on a private vps."
        ).add_fields(
            stats.items(),
            map_title=lambda name: name.upper(),
            map_values=lambda percent, info, unit: (
                f"> `{percent:.3f}` **%**\n- `{info}` **{unit}**"
            )
        )

    @command(
        name="invite",
        guild=TEST_GUILD_ID
        # aliases=("inv", "i"),
        # brief="A link to invite the bot"
    )
    async def invite(self) -> p_Embed:
        """Command to get bot invitation link."""
        return p_Embed(
            title="Invite the Bot !",
            description=(
                "> Click this link to invite this bot on your servers !\n"
                "You need to have the required permissions on the server.\n"
                "[invite me now](https://discord.com/api/oauth2/authorize"
                f"?client_id={self.client.bot}&permissions=8&scope=bot)"
            )
        )


setup = InfoCog
