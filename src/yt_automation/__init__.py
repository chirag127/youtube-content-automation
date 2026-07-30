"""yt_automation — YouTube automation via Selenium element selectors + Data API v3."""

from .base import BaseAutomation
from .comments import CommentBot
from .driver import build_driver, wait
from .playback import PlaybackController
from .reporting import ReportManager
from .search import SearchClient
from .subscriptions import SubscriptionManager
from .watch_later import WatchLaterManager

__all__ = [
    "BaseAutomation",
    "CommentBot",
    "PlaybackController",
    "ReportManager",
    "SearchClient",
    "SubscriptionManager",
    "WatchLaterManager",
    "build_driver",
    "wait",
]
