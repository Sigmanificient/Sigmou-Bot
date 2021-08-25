from __future__ import annotations

import random

import embed_templator

from app.utils.humanify import pretty_time_small
from app.utils.timer import time


class Embed(embed_templator.Embed):
    """Embed wrapping of discord.Embed class."""

    def setup(self) -> Embed:
        return self.set_author(
            name=f"Requested by {self.ctx.author} 🚀",
            icon_url=self.ctx.author.avatar_url
        )

    def update(self) -> Embed:
        lucky: str = (
            "There was 1 / 1 000 000 chance for this message to show 🍀"
        ) * (not random.randint(0, 1_000_000))

        self.set_footer(
            icon_url=self.client.user.avatar_url,
            text=lucky or '   '.join(
                (
                    f"⚙️ {pretty_time_small(time(self.ctx.time, keep=True))}",
                    f"⏳ {pretty_time_small(self.client.latency)}",
                    f"🔑 {self.ctx.prefix}help",
                )
            )
        )

        time(self.ctx.time)
        return self
