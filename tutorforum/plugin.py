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
    "username": {% if MONGODB_USERNAME %}"{{ MONGODB_USERNAME }}"{% else %}None{% endif %},
    "password": {% if MONGODB_PASSWORD %}"{{ MONGODB_PASSWORD }}"{% else %}None{% endif %},
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

# Enable forum v2
tutor_hooks.Filters.CLI_DO_INIT_TASKS.add_item(
    (
        "lms",
        """
(./manage.py lms waffle_flag --list | grep discussions.enable_forum_v2) || ./manage.py lms waffle_flag --create --everyone discussions.enable_forum_v2

# Switch to MySQL backend, unless a global waffle flag was already created.
# This allows user to stick to the MongoDb backend by creating a flag with:
#
#     ./manage.py lms waffle_flag --create --deactivate forum_v2.enable_mysql_backend
#
./manage.py lms shell -c "
from waffle.models import Flag
flag, created = Flag.objects.get_or_create(name='forum_v2.enable_mysql_backend')
if created:
    print('Configuring MySQL backend for forum data storage')
    flag.everyone = True
    flag.save()
elif not flag.everyone:
    print('⚠️ You should migrate your forum data to MySQL: https://github.com/overhangio/tutor-forum/#installation')
else:
    print('MySQL backend already configured for forum data storage')"

# Initialize indices
./manage.py lms initialize_forum_indices

# Create Mongodb indexes
./manage.py lms forum_create_mongodb_indexes
""",
    )
)

# Add configuration entries
tutor_hooks.Filters.CONFIG_DEFAULTS.add_items(
    [(f"FORUM_{key}", value) for key, value in config.get("defaults", {}).items()]
)
