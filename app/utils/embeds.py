from __future__ import annotations

import random
from time import time as epoch_unix
from typing import Any, Callable, Dict, Iterable, Optional, Union, TYPE_CHECKING

from app.timed_ctx import TimedCtx
from app.utils.timer import time
from app.utils.humanify import pretty_time, pretty_time_small

if TYPE_CHECKING:
    from app.bot import Bot

import discord


class Embed(discord.Embed):
    """Embed wrapping of discord.Embed class."""

    @classmethod
    def load(cls, client: Bot):
        """Set the client instance."""
        cls.client: Bot = client

    def __init__(self, ctx: Optional[TimedCtx]):
        """Initialise discord embed, set default bot color and set dynamic footer if ctx is passed."""
        if not self.client:
            raise RuntimeError("Embed hasn't been initialized yet.")

        self.ctx = ctx

    def __call__(self, **kwargs) -> Embed:
        super().__init__(**kwargs, colour=getattr(self.client, 'colour', self.client.user.colour))

        if self.ctx is not None:
            self.set_author(
                name=f"Requested by {self.ctx.author} 🚀",
                icon_url=self.ctx.author.avatar_url
            )

        return self

    def update_footer(self) -> Embed:
        lucky: str = "There was 1 / 1 000 000 chance for this message to show 🍀" * (not random.randint(0, 1_000_000))

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

        return self

    def to_dict(self):
        self.update_footer()
        return super().to_dict()

    def add_fields(
            self,
            field_list: Union[Dict[Any, Any], Iterable[Iterable[Any, Any]]],
            checks: Optional[Callable[[Any], Any]] = bool,
            map_title: Optional[Callable[[Any], str]] = str,
            map_values: Optional[Callable[[Any], str]] = str,
            inline: bool = True
    ) -> Embed:
        """Add multiple fields from a list, dict or generator of fields with possible mapping."""
        if isinstance(field_list, dict):
            field_list = field_list.items()

        for field_name, field_value in field_list:
            val = map_values(field_value)
            if checks(val):
                self.add_field(
                    name=map_title(field_name),
                    value=map_values(field_value),
                    inline=inline
                )

        return self

    def __del__(self):
        time(self.ctx.time)
