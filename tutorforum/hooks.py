"""
These hooks are stored in a separate module. If they were included in plugin.py, then
the tutor-forum hooks would be created in the context of some other plugin that imports
them.
"""
from __future__ import annotations

from tutor.core.hooks import Filter

FORUM_ENV: Filter[dict[str, str], []] = Filter()
