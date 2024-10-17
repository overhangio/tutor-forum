from __future__ import annotations

from tutor import hooks as tutor_hooks
from tutor.__about__ import __version_suffix__

from .__about__ import __version__

# Handle version suffix in nightly mode, just like tutor core
if __version_suffix__:
    __version__ += "-" + __version_suffix__

config = {
    "defaults": {
        "VERSION": __version__,
    },
}

# Auto-mount forum repository
tutor_hooks.Filters.MOUNTED_DIRECTORIES.add_item(("openedx", "forum"))

tutor_hooks.Filters.ENV_PATCHES.add_items(
    [
        # Patch edx-platform
        # https://github.com/openedx/edx-platform/pull/35671
        # TODO after this PR has been merged, remove this patch
        (
            "openedx-dockerfile-post-git-checkout",
            """
RUN git remote add edly https://github.com/edly-io/edx-platform \
    && git fetch edly edly/forumv2 \
    && git merge edly/edly/forumv2""",
        ),
        # Enable forum feature
        (
            "openedx-common-settings",
            """FEATURES["ENABLE_DISCUSSION_SERVICE"] = True""",
        ),
    ]
)

# Enable forum v2
tutor_hooks.Filters.CLI_DO_INIT_TASKS.add_item(
    (
        "lms",
        # TODO at some point, maybe this flag will be renamed to "forum_v2.enable".
        """
(./manage.py lms waffle_flag --list | grep forum_v2.enable_forum_v2) || ./manage.py lms waffle_flag --create --everyone forum_v2.enable_forum_v2
(./manage.py lms waffle_flag --list | grep forum_v2.enable_mysql_backend) || ./manage.py lms waffle_flag --create --everyone forum_v2.enable_mysql_backend
""",
    )
)

# Add configuration entries
tutor_hooks.Filters.CONFIG_DEFAULTS.add_items(
    [(f"FORUM_{key}", value) for key, value in config.get("defaults", {}).items()]
)
