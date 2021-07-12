from os import listdir
from typing import Dict, Tuple, NoReturn, Optional

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
    async def help_command(self, ctx: TimedCtx, command: Optional[str] = None) -> None:
        await ctx.send("Nope.")

    @commands.command(
        name='cmds',
        aliases=('all', 'all_cmds'),
        brief="List every command osf the bot"
    )
    @commands.cooldown(2, 60, commands.BucketType.user)
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
