from discord import app_commands, TextChannel, Interaction
from discord.ext import commands


@app_commands.guild_only()
class ModerationCommandsGroup(app_commands.Group, name="mod"):

    @app_commands.command(name="purge")
    async def purge(self, interaction: Interaction, limit: int = 0):
        if (channel := interaction.channel) is None:
            await interaction.response.send_message(
                "You cannot perform this action outside a channel :<"
            )
            return

        if not isinstance(channel, TextChannel):
            await interaction.response.send_message(
                "You cannot perform this action outside a text channel :<"
            )

        deleted = await channel.purge(limit=limit or float('inf'))
        await channel.send(f'> Deleted `{len(deleted)}` message(s)')


async def setup(client: commands.Bot):
    client.tree.add_command(ModerationCommandsGroup())
