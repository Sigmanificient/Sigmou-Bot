from typing import NoReturn, Optional

from discord.ext import commands

from app.utils.timed_ctx import TimedCtx
from app.bot import Bot


class ModerationCog(commands.Cog):
    """Admin and Moderator utils command."""

    def __init__(self, client: Bot):
        """Link to bot instance."""
        self.client: Bot = client

    @commands.command(
        name="purge",
        description=(
            "Clear the number of messages asked. If no number is given, "
            "clear all message in the channel. "
        ),
        aliases=('clear', 'cls'),
        brief="the sample",
    )
    async def purge_command(
        self, ctx: TimedCtx, limit: Optional[int] = None
    ) -> None:
        """Clear the number of messages asked. If no number is given,
            clear all message in the channel. """

        await ctx.channel.purge(limit=limit)
        await ctx.send("Purged !")


def setup(client: Bot) -> NoReturn:
    client.add_cog(ModerationCog(client))
