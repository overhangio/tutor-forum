from __future__ import annotations

from tutor import hooks as tutor_hooks
from tutor.__about__ import __version_suffix__

from .__about__ import __version__

# Handle version suffix in main mode, just like tutor core
if __version_suffix__:
    __version__ += "-" + __version_suffix__

config = {
    "defaults": {
        "VERSION": __version__,
    },
}

# Auto-mount forum repository
tutor_hooks.Filters.MOUNTED_DIRECTORIES.add_item(("openedx", "forum"))

tutor_hooks.Filters.ENV_PATCHES.add_item(
    # Enable forum feature
    (
        "openedx-common-settings",
        """# Forum configuration
FORUM_SEARCH_BACKEND = "forum.search.meilisearch.MeilisearchBackend"
FEATURES["ENABLE_DISCUSSION_SERVICE"] = True
# Forum mongodb configuration, for existing platforms still running mongodb
FORUM_MONGODB_DATABASE = "cs_comments_service"
FORUM_MONGODB_CLIENT_PARAMETERS = {
    "host": "{{ MONGODB_HOST }}",
    "port": {{ MONGODB_PORT }},
    {% if MONGODB_USERNAME %}"username": "{{ MONGODB_USERNAME }}",{% endif %}
    {% if MONGODB_PASSWORD %}"password": "{{ MONGODB_PASSWORD }}",{% endif %}
    "ssl": {{ MONGODB_USE_SSL }},
}
{}
{% if MONGODB_AUTH_MECHANISM %}
FORUM_MONGODB_CLIENT_PARAMETERS["authMechanism"] = "{{ MONGODB_AUTH_MECHANISM }}"
{% endif %}
{% if MONGODB_AUTH_SOURCE %}
FORUM_MONGODB_CLIENT_PARAMETERS["authSource"] = "{{ MONGODB_AUTH_SOURCE }}"
{% endif %}
{% if MONGODB_REPLICA_SET %}
FORUM_MONGODB_CLIENT_PARAMETERS["replicaSet"] = "{{ MONGODB_REPLICA_SET }}"
{% endif %}
""",
    )
)

# Initialize forum indices
tutor_hooks.Filters.CLI_DO_INIT_TASKS.add_item(
    (
        "lms",
        """
./manage.py lms initialize_forum_indices
""",
    )
)

# Add configuration entries
tutor_hooks.Filters.CONFIG_DEFAULTS.add_items(
    [(f"FORUM_{key}", value) for key, value in config.get("defaults", {}).items()]
)
