import inspect
from os import listdir
from typing import Dict, Tuple, NoReturn, List

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
                description=f"> This is the whole code structure of {self.client.user.name}!"
            ).add_fields(
                self.files_info,
                map_title=lambda name: f"📝 {name}" if name != "Total" else "📊 Total",
                map_values=lambda file: "`%s` characters\n `%s` lines" % (f"{len(file):,}", len(file.splitlines())),
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
                command for command in cog.get_commands() if await self.is_visible(ctx, command)
            ]

            if len(available_commands):
                all_commands[cog_name] = available_commands.copy()
                total += len(available_commands)

        aliases: int = len(self.client.all_commands) - len(self.client.commands)

        await ctx.send(
            embed=Embed(ctx)(
                title=f"General Help {self.client.user.name}",
                description=f"- `{total}`/`{len(self.client.commands)}` available commands\n`{aliases}` aliases"
            ).add_fields(
                all_commands,
                map_values=lambda cog_commands: ', '.join(f"`{command.name}`" for command in cog_commands),
                inline=False
            )
        )

    @commands.command(
        name="help",
        description="A command to find ever information about an other command",
        brief="The global help command"
    )
    async def help_command(self, ctx: TimedCtx) -> None:
        await ctx.invoke(self.help_command_default)

    @commands.command(
        name='cmds',
        aliases=('all', 'all_cmds'),
        brief="List every command osf the bot"
    )
    async def all_commands(self, ctx: TimedCtx) -> None:
        """
        Provide a list of every command available command for the user,
        split by extensions and organized in alphabetical order.
        Will not show the event-only extension
        """
        await ctx.send(
            embed=Embed(ctx)(
                title='All commands',
                description=f"> `{len(self.client.commands)}` commands available"
            ).add_fields(
                self.client.cogs.items(), checks=len,
                map_title=lambda cog_name: cog_name.capitalize(),
                map_values=lambda cog: '  •  '.join(sorted(f'`{c.name}`' for c in cog.get_commands())),
                inline=False
            )
        )


def setup(client: Bot) -> NoReturn:
    client.add_cog(InfoCog(client))
