from __future__ import annotations

from typing import TYPE_CHECKING

from discord import app_commands, Interaction, Embed
from discord.ext import commands

if TYPE_CHECKING:
    from sigmou.bot import Bot

from sigmou.constants import TEST_GUILD_ID
from sigmou.utils.db_wrapper import db


@app_commands.guild_only()
class GameCommandsGroup(app_commands.Group, name="game"):

    @app_commands.command(name="start")
    async def start_command(self, interaction: Interaction):
        user = await db.fetchone(
            "select true from users where discord_id = ?",
            interaction.user.id
        )

        if user:
            await interaction.response.send_message(
                embed=Embed(
                    title="Error",
                    description="You already have an account !"
                )
            )
            return

        await db.post(
            "insert into users(discord_id) values (?)",
            interaction.user.id
        )

        await interaction.response.send_message(
            embed=Embed(
                title="Welcome !",
                description="Your account has just been created !"
            )
        )

    @app_commands.command(name="daily")
    async def daily_command(self, interaction: Interaction):
        user = await db.fetchone(
            "select true from users where discord_id = ?",
            interaction.user.id
        )

        if not user:
            await interaction.response.send_message(
                embed=Embed(
                    title="Error",
                    description="You dont have an account !"
                )
            )
            return

        await db.post(
            "UPDATE users SET point = point + 100 WHERE discord_id = ?",
            interaction.user.id,
        )

        await interaction.response.send_message(
            "You received your daily points, enjoy !"
        )

    @app_commands.command(name="profile")
    async def profile_command(self, interaction: Interaction):
        user = interaction.user

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
                f"`{await self.client.get_user(user)}`: {point:,}"
                for (user, point) in (
                    await db.fetchall(
                        "select discord_id, point from users "
                        "order by point desc limit 10"
                    )
                )
            )
        )


async def setup(client: commands.Bot):
    client.tree.add_command(GameCommandsGroup())
