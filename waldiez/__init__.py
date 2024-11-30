"""Harmony package."""

from ._version import __version__
from .conflict_checker import check_conflicts
from .exporter import HarmonyExporter
from .models import Harmony
from .runner import HarmonyRunner

# flag to check if ag2 and autogen-agentchat
# are installed at the same time
__WALDIEZ_CHECKED_FOR_CONFLICTS = False


def _check_conflicts_once() -> None:
    """Check for conflicts once."""
    # pylint: disable=global-statement
    global __WALDIEZ_CHECKED_FOR_CONFLICTS
    if __WALDIEZ_CHECKED_FOR_CONFLICTS is False:
        check_conflicts()
        __WALDIEZ_CHECKED_FOR_CONFLICTS = True


_check_conflicts_once()


__all__ = [
    "Harmony",
    "HarmonyExporter",
    "HarmonyRunner",
    "__version__",
]
