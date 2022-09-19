import re

from discord import app_commands, TextChannel, Interaction
from discord.ext import commands


@app_commands.guild_only()
class DevCommandsGroup(app_commands.Group, name="dev"):

    @app_commands.command(name="purge_fox")
    async def purge_fox(self, interaction: Interaction):
        if interaction.user.id != 812699388815605791:
            await interaction.response.send_message("No u")
            return

        if (channel := interaction.channel) is None:
            await interaction.response.send_message(
                "You cannot perform this action outside a channel :<"
            )
            return

        if not isinstance(channel, TextChannel):
            await interaction.response.send_message(
                "You cannot perform this action outside a text channel :<"
            )

        deleted = await channel.purge(
            check=lambda m: m.author.id == interaction.client.user.id
        )

        await channel.send(f'> Deleted `{len(deleted)}` message(s)')

    @app_commands.command(name="regex")
    async def pretty_regex(self, interaction: Interaction, regex: str):
        # todo: fix the hell out of this
        ansi = {
            'red': '[0m[31m',
            'green': '[0m[32m',
            'orange': '[0m[33m',
            'blue': '[0m[34m',
            'pink': '[0m[35m',
            'cyan': '[0m[36m',
            'white': '[0m'
        }

        save = regex[:]
        q = False

        out = ''
        s = False

        for char in regex:
            if s:
                s = False
                out += char
                continue

            if q and char.isdigit():
                out += ansi['orange'] + char

            elif q and char == ',':
                out += ansi['white'] + char

            elif char in '[]{}':
                out += ansi['blue'] + char
                q = char == '{'

            elif char in '()':
                out += ansi['white'] + char

            elif char in '^|$':
                out += ansi['pink'] + char

            elif char in '+*?':
                out += ansi['orange'] + char

            elif char == '\\':
                out += ansi['red'] + char
                s = True

            else:
                out += ansi['cyan'] + char

        await interaction.response.send_message(
            f"> `{save}`:\n```ansi\n{out}\n```"
        )
