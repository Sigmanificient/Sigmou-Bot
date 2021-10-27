from os import listdir
from typing import Dict, Tuple

import psutil
from pincer import command
from pincer.objects import Embed

from app.bot import Bot
from app.constants import TEST_GUILD_ID


class InfoCog:
    """A simple commands cog template."""

    def __init__(self, client: Bot):
        """Link to bot instance."""
        self.client: Bot = client

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

    @command(name="code_stats", guild=TEST_GUILD_ID)
    async def code_command(self) -> Embed:
        return Embed(
            title="Code Structure",
            description=(
                "> This is the whole code structure of "
                f"{self.client.bot.username}!"
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

    @command(
        name="panel",
        guild=TEST_GUILD_ID
    )
    async def panel_stats(self) -> Embed:
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

        return Embed(
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
    async def invite(self) -> Embed:
        """Command to get bot invitation link."""
        return Embed(
            title="Invite the Bot !",
            description=(
                "> Click this link to invite this bot on your servers !\n"
                "You need to have the required permissions on the server.\n"
                "[invite me now](https://discord.com/api/oauth2/authorize"
                f"?client_id={self.client.bot}&permissions=8&scope=bot)"
            )
        )


setup = InfoCog
