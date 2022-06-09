from glob import glob
import os
import pkg_resources

from tutor import hooks as tutor_hooks

from .__about__ import __version__


config = {
    "defaults": {
        "VERSION": __version__,
        "DOCKER_IMAGE": "{{ DOCKER_REGISTRY }}overhangio/openedx-forum:{{ FORUM_VERSION }}",
        "MONGODB_DATABASE": "cs_comments_service",
        "PORT": "4567",
        "API_KEY": "forumapikey",
    },
}

tutor_hooks.Filters.COMMANDS_INIT.add_item((
    "forum",
    ("forum", "tasks", "forum", "init"),
))

tutor_hooks.Filters.IMAGES_BUILD.add_item((
    "forum",
    ("plugins", "forum", "build", "forum"),
    "{{ FORUM_DOCKER_IMAGE }}",
    (),
))
tutor_hooks.Filters.IMAGES_PULL.add_item((
    "forum",
    "{{ FORUM_DOCKER_IMAGE }}",
))
tutor_hooks.Filters.IMAGES_PUSH.add_item((
    "forum",
    "{{ FORUM_DOCKER_IMAGE }}",
))

# Add the "templates" folder as a template root
tutor_hooks.Filters.ENV_TEMPLATE_ROOTS.add_item(
    pkg_resources.resource_filename("tutorforum", "templates")
)
# Render the "build" and "apps" folders
tutor_hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    [
        ("forum/build", "plugins"),
        ("forum/apps", "plugins"),
    ],
)
# Load patches from files
for path in glob(
    os.path.join(
        pkg_resources.resource_filename("tutorforum", "patches"),
        "*",
    )
):
    with open(path, encoding="utf-8") as patch_file:
        tutor_hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))
# Add configuration entries
tutor_hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        (f"FORUM_{key}", value)
        for key, value in config.get("defaults", {}).items()
    ]
)
tutor_hooks.Filters.CONFIG_OVERRIDES.add_items(list(config.get("overrides", {}).items()))
