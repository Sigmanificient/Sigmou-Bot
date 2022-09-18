from .connection import on_ready
from .messages import on_message


events = (on_ready, on_message,)
__all__ = ('events',)
