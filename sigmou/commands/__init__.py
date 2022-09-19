from .dev import DevCommandsGroup
from .info import InfoCommandsGroup
from .leveling import LevelCommandsGroup
from .moderation import ModerationCommandsGroup


groups = (
    DevCommandsGroup,
    InfoCommandsGroup,
    LevelCommandsGroup,
    ModerationCommandsGroup
)

__all__ = ('groups',)
