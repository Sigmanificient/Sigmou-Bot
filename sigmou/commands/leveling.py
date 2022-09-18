from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from discord import app_commands, Interaction, Embed, Member, User
from discord.ext import commands

if TYPE_CHECKING:
    from sigmou.bot import Bot

from sigmou.utils.db_wrapper import db


@app_commands.guild_only()
class GameCommandsGroup(app_commands.Group, name="level"):

    @app_commands.command(name="profile")
    async def profile_command(
        self, interaction: Interaction,
        user: Optional[User] = None
    ):
        user = interaction.user if user is None else user

        user_exists = await db.fetchone(
            "select true from users where discord_id = ?", user.id
        )

        if not user_exists:
            await interaction.response.send_message(
                embed=Embed(
                    title="Error",
                    description=(
                        f"{'You' if user.id == interaction.user.id else user} "
                        "dont have an account !"
                    )
                )
            )
            return

        point = await db.fetchone(
            "select point from users where discord_id = ?", user.id
        )

        await interaction.response.send_message(
            f"> {'You' if user == interaction.user.id else user} "
            f"have `{point or 0}` points !"
        )

    @app_commands.command(name="leaderboard")
    async def leaderboard(self, interaction: Interaction):
        await interaction.response.send_message(
            "\n".join(
                f"`{c}` - {interaction.client.get_user(user)} - {point:,}"
                for c, (user, point) in enumerate(
                    await db.fetchall(
                        "select discord_id, point from users "
                        "order by point desc limit 10"
                    ), start=1
                )
            )
        )


async def setup(client: commands.Bot):
    client.tree.add_command(GameCommandsGroup())
