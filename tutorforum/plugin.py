from glob import glob
import os
import pkg_resources
import urllib.parse

from tutor import hooks as tutor_hooks

from .__about__ import __version__


config = {
    "defaults": {
        "VERSION": __version__,
        "DOCKER_IMAGE": "{{ DOCKER_REGISTRY }}overhangio/openedx-forum:{{ FORUM_VERSION }}",
        "MONGODB_DATABASE": "cs_comments_service",
        "PORT": "4567",
        "API_KEY": "forumapikey",
        "REPOSITORY": "https://github.com/openedx/cs_comments_service.git",
        "REPOSITORY_VERSION": "{{ OPENEDX_COMMON_VERSION }}",
    },
}

tutor_hooks.Filters.COMMANDS_INIT.add_item(
    (
        "forum",
        ("forum", "tasks", "forum", "init"),
    )
)

tutor_hooks.Filters.IMAGES_BUILD.add_item(
    (
        "forum",
        ("plugins", "forum", "build", "forum"),
        "{{ FORUM_DOCKER_IMAGE }}",
        (),
    )
)
tutor_hooks.Filters.IMAGES_PULL.add_item(
    (
        "forum",
        "{{ FORUM_DOCKER_IMAGE }}",
    )
)
tutor_hooks.Filters.IMAGES_PUSH.add_item(
    (
        "forum",
        "{{ FORUM_DOCKER_IMAGE }}",
    )
)


@tutor_hooks.Filters.COMPOSE_MOUNTS.add()
def _mount_cs_comments_service(volumes, name):
    """
    When mounting cs_comments_service with `--mount=/path/to/cs_comments_service`,
    bind-mount the host repo in the forum container.
    """
    if name == "cs_comments_service":
        path = "/app/cs_comments_service"
        volumes += [
            ("forum", path),
            ("forum-job", path),
        ]
    return volumes


# Add the "templates" folder as a template root
tutor_hooks.Filters.ENV_TEMPLATE_ROOTS.add_item(
    pkg_resources.resource_filename("tutorforum", "templates")
)


def auth_mech_as_ruby(auth_mech):
    """
    Convert the authentication mechanism from the format
    specified for the Python version to the Ruby version.

    https://pymongo.readthedocs.io/en/stable/api/pymongo/database.html#pymongo.auth.MECHANISMS
    https://github.com/mongodb/mongo-ruby-driver/blob/932b06b7564a5e5ae8d4ad08fe8d6ceee629e4eb/lib/mongo/auth.rb#L69
    """
    return {
        "GSSAPI": ":gssapi",
        "MONGODB-AWS": ":aws",
        "MONGODB-CR": ":mongodb_cr",
        "MONGODB-X509": ":mongodb_x509",
        "PLAIN": ":plain",
        "SCRAM-SHA-1": ":scram",
        # SCRAM-256 is only supported from v2.6 of the ruby driver onwards.
        # See https://github.com/mongodb/mongo-ruby-driver/releases/tag/v2.6.0
        "SCRAM-SHA-256": ":scram",
    }.get(auth_mech) or ""


def forum_mongodb_host(host: str) -> str:
    """
    Remove the querystring parameters from the mongodb host url. These parameters are
    not supported by the outdated mongodb gem. Thus we just trim them out.
    """
    # 0 = scheme
    # 1 = netloc
    # 2 = path
    # 3 = params
    # 4 = query
    # 5 = fragment
    parsed = [*urllib.parse.urlparse(host)]
    parsed[4] = ""
    # We also remove the trailing "/" from the path, which will not play well with the
    # full url where we concatenate the database name.
    parsed[2] = parsed[2].rstrip("/")
    return urllib.parse.urlunparse(parsed)


tutor_hooks.Filters.ENV_TEMPLATE_FILTERS.add_items(
    [
        ("auth_mech_as_ruby", auth_mech_as_ruby),
        ("forum_mongodb_host", forum_mongodb_host),
    ]
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
        tutor_hooks.Filters.ENV_PATCHES.add_item(
            (os.path.basename(path), patch_file.read())
        )
# Add configuration entries
tutor_hooks.Filters.CONFIG_DEFAULTS.add_items(
    [(f"FORUM_{key}", value) for key, value in config.get("defaults", {}).items()]
)
tutor_hooks.Filters.CONFIG_OVERRIDES.add_items(
    list(config.get("overrides", {}).items())
)
