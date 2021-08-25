import asyncio
from typing import NoReturn, Optional

from discord.ext import commands
from discord_components import Button, ButtonStyle

from app.utils.embeds import Embed
from app.utils.timed_ctx import TimedCtx
from app.bot import Bot


class ModerationCog(commands.Cog):
    """Admin and Moderator utils command."""

    def __init__(self, client: Bot):
        """Link to bot instance."""
        self.client: Bot = client
        Embed.load(self.client)

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

        delete_amount = limit if limit is not None else 'all'

        purge_embed = Embed(ctx)(
            title="Purge Channel",
            description=(
                f"Are you sure to delete {delete_amount} messages?\n"
                "> click the button below to confirm *(timeout in 10s)*"
            )
        )

        message = await ctx.send(
            embed=purge_embed,
            components=[
                Button(
                    label="Purge !",
                    custom_id="purge",
                    style=ButtonStyle.red,
                    emoji="🧨"
                )
            ]
        )

        try:
            await self.client.wait_for(
                "button_click",
                check=lambda i: (
                    i.message == message and i.author == ctx.author
                ),
                timeout=10
            )
        except asyncio.exceptions.TimeoutError:
            await message.edit(
                embed=purge_embed(
                    title="Time Out",
                    description=f"**{ctx.author}** did not confirmed the purge"
                ),
                components=[]
            )
            return

        await ctx.channel.purge(limit=limit)

        await ctx.send(
            embed=purge_embed(
                title="Purged !",
                description=f"**{ctx.author}** did not confirmed the purge"
            ),
            components=[],
            delete_after=5
        )


def setup(client: Bot) -> NoReturn:
    client.add_cog(ModerationCog(client))
