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

    @staticmethod
    async def is_visible(ctx: TimedCtx, command: commands.Command) -> bool:
        """Check whether a command is visible for an user"""
        if not len(command.checks):
            return True

        for check in command.checks:
            try:
                if inspect.iscoroutinefunction(check):
                    await check(ctx)
                else:
                    check(ctx)

            except commands.errors.CheckFailure:
                return False

        return True

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

    @commands.command(
        name="help",
        description="A command to find ever information about an other command",
        brief="The global help command"
    )
    async def help_command_default(self, ctx: TimedCtx) -> None:
        all_commands: Dict[str: List[commands.Command]] = {}
        total: int = 0

        for cog_name, cog in self.client.cogs.items():
            available_commands: List[commands.Command] = [
                command
                for command in cog.get_commands()
                if await self.is_visible(ctx, command)
            ]

            if len(available_commands):
                all_commands[cog_name] = available_commands.copy()
                total += len(available_commands)

        aliases: int = len(self.client.all_commands) - len(self.client.commands)

        await ctx.send(
            embed=Embed(ctx)(
                title=f"General Help {self.client.user.name}",
                description=(
                    f"- `{total}`/`{len(self.client.commands)}` "
                    f"available commands\n`{aliases}` aliases"
                )
            ).add_fields(
                all_commands,
                map_values=lambda cog_commands: ', '.join(
                    f"`{command.name}`" for command in cog_commands
                ),
                inline=False
            )
        )

    @command(
        name="panel",
        guild=TEST_GUILD_ID
        # aliases=('pan',),
        # brief="Some data about the panel"
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
