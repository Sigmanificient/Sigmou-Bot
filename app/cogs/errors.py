from typing import NoReturn

import discord
from discord.ext import commands

from app.bot import Bot
from app.utils.humanify import pretty_time
from app.utils.timed_ctx import TimedCtx


class LoggingCog(commands.Cog):
    """Global Error reporting cog."""

    def __init__(self, client: Bot):
        """Link to bot instance."""
        self.client: Bot = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx: TimedCtx, error: Exception) -> None:
        if isinstance(error, discord.ext.commands.BadArgument):
            await ctx.send(
                "> Une erreur est survenue sur un des paramètres de la commande"
            )

            return

        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.send(
                "Your are on cooldown."
                f" Please wait {pretty_time(error.retry_after)}"
            )

            return

        await ctx.send(f"**Error report for command `{ctx.command}`**")
        await ctx.send(f"```{error}```")
        await ctx.send(f"```{error!r}```")


setup = LoggingCog
