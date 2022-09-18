from .dev import DevCommandsGroup
from .info import InfoCommandsGroup
from .leveling import LevelCommandsGroup
from .moderation import ModerationCommandsGroup
from .time import TimeCommandsGroup


groups = (
    DevCommandsGroup,
    InfoCommandsGroup,
    LevelCommandsGroup,
    ModerationCommandsGroup,
    TimeCommandsGroup
)

__all__ = ('groups',)
