from __future__ import annotations

from os import listdir
from typing import TYPE_CHECKING, Dict, Tuple

import psutil
from discord import app_commands, Interaction, Embed
from discord.ext import commands

if TYPE_CHECKING:
    from sigmou.bot import Bot


@app_commands.guild_only()
class InfoCommandsGroup(app_commands.Group, name="info"):
    def __init__(self):
        super().__init__()

        self.files_info: Dict[str, str] = {}
        folders: Tuple[str, ...] = (".", "sigmou", "sigmou/commands")

        for file, path in {
            _f: path
            for path in folders
            for _f in listdir(path)
            if _f.endswith(".py")
        }.items():
            with open(f"{path}/{file}", encoding="utf-8") as f:
                self.files_info[file.replace('_', r'\_')] = f.read()

        self.files_info["Total"] = "\n".join(self.files_info.values())

    @app_commands.command(name="code")
    async def code_command(self, interaction: Interaction):
        embed = Embed(
            title="Code Structure",
            description=(
                "> This is the whole code structure of "
                f"{interaction.client.user.name}!"
            ),
        )

        for file, lines in self.files_info.items():
            embed.add_field(
                name=f"📝 {file}" if file != "Total" else "📊 Total",
                value=(
                    f"`{len(lines)}` characters"
                    f"\n `{len(lines.splitlines())}` lines"
                )
            )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="panel")
    async def panel_stats(self, interaction: Interaction):
        mb: int = 1024**2

        vm = psutil.virtual_memory()
        cpu_freq = psutil.cpu_freq()
        cpu_percent = psutil.cpu_percent()
        disk = psutil.disk_usage(".")

        stats = {
            "ram": (
                100 * (vm.used / vm.total),
                f"{(vm.total / mb) / 1000:,.3f}", "Gb"
            ),
            "cpu": (
                cpu_percent,
                f"{cpu_freq.current / 1000:.1f}`/`{cpu_freq.max / 1000:.1f}",
                "Ghz",
            ),
            "disk": (
                100 * (disk.used / disk.total),
                f"{disk.total / mb:,.0f}", "Mb"
            ),
        }

        embed = Embed(
            title="Server Report",
            description="The bot is hosted on a private vps."
        )

        for name, (percent, info, unit) in stats.items():
            embed.add_field(
                name=name.upper(),
                value=f"> `{percent:.3f}` **%**\n- `{info}` **{unit}**"
            )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="invite")
    async def invite(self, interaction: Interaction):
        uid = interaction.client.user.id
        await interaction.response.send_message(
            embed=Embed(
                title="Invite the Bot !",
                description=(
                    "> Click this link to invite this bot on your servers !\n"
                    "You need to have the required permissions on the server.\n"
                    "[invite me now](https://discord.com/api/oauth2/authorize"
                    f"?client_id={uid}&scope=bot%20applications.commands"
                    "&permissions=8)"
                ),
            )
        )


async def setup(client: commands.Bot):
    client.tree.add_command(InfoCommandsGroup())
