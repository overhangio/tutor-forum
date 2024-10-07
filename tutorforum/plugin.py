from __future__ import annotations

import os
import urllib.parse
from glob import glob

import importlib_resources
from tutor import hooks as tutor_hooks
from tutor.__about__ import __version_suffix__

from .__about__ import __version__
from .hooks import FORUM_ENV

# Handle version suffix in nightly mode, just like tutor core
if __version_suffix__:
    __version__ += "-" + __version_suffix__

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

FORUM_ENV_BASE: dict[str, str] = {
    "SEARCH_SERVER": "{{ ELASTICSEARCH_SCHEME }}://{{ ELASTICSEARCH_HOST }}:{{ ELASTICSEARCH_PORT }}",
    "MONGODB_AUTH": "{{ get_mongo_auth(MONGODB_USERNAME, MONGODB_PASSWORD) }}",
    "MONGODB_HOST": "{{ MONGODB_HOST|forum_mongodb_host }}",
    "MONGODB_PORT": "{{ MONGODB_PORT }}",
    "MONGODB_DATABASE": "{{ FORUM_MONGODB_DATABASE }}",
    "MONGOID_AUTH_SOURCE": "{{ MONGODB_AUTH_SOURCE }}",
    "MONGOID_AUTH_MECH": "{{ MONGODB_AUTH_MECHANISM|auth_mech_as_ruby }}",
    "MONGOID_USE_SSL": "{{ 'true' if MONGODB_USE_SSL else 'false' }}",
    "MONGOHQ_URL": "{{ get_mongohq_url(MONGODB_HOST, MONGODB_PORT,MONGODB_DATABASE, get_mongo_auth(MONGODB_USERNAME, MONGODB_PASSWORD)) }}",
}

with open(
    str(
        importlib_resources.files("tutorforum")
        / os.path.join("templates", "forum", "tasks", "forum", "init")
    ),
    encoding="utf8",
) as f:
    tutor_hooks.Filters.CLI_DO_INIT_TASKS.add_item(("forum", f.read()))

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


def get_mongohq_url(
    mongo_host: str, mongo_port: str, mongo_database: str, mongo_auth: str
) -> str:
    """
    Used to return mongo, to handle the special case when mongodb+srv used
    For more info look at the following PR https://github.com/overhangio/tutor-forum/pull/10
    """
    if "mongodb+srv" in mongo_host:
        return f"{mongo_host}/{mongo_database}"
    return f"{mongo_auth}{mongo_host}:{mongo_port}/{mongo_database}"


def get_mongo_auth(monogo_username: str, mongo_password: str) -> str:
    if monogo_username and mongo_password:
        return f"{monogo_username}:{mongo_password}@"
    return ""


tutor_hooks.Filters.ENV_TEMPLATE_VARIABLES.add_items(
    [("get_mongohq_url", get_mongohq_url), ("get_mongo_auth", get_mongo_auth)]
)


# Bind-mount repo at runtime
@tutor_hooks.Filters.COMPOSE_MOUNTS.add()
def _mount_cs_comments_service(
    volumes: list[tuple[str, str]], name: str
) -> list[tuple[str, str]]:
    """
    When mounting cs_comments_service with `--mount=/path/to/cs_comments_service`,
    bind-mount the host repo in the forum container.
    """
    if name == "cs_comments_service":
        repo_path = "/app/cs_comments_service"
        volumes += [
            ("forum", repo_path),
            ("forum-job", repo_path),
        ]
    return volumes


# Bind-mount repo at build-time
@tutor_hooks.Filters.IMAGES_BUILD_MOUNTS.add()
def _mount_forum_on_build(
    mounts: list[tuple[str, str]], host_path: str
) -> list[tuple[str, str]]:
    path_basename = os.path.basename(host_path)
    if path_basename == "cs_comments_service":
        mounts.append(("forum", "forum-src"))
    return mounts


# Add the "templates" folder as a template root
tutor_hooks.Filters.ENV_TEMPLATE_ROOTS.add_item(
    str(importlib_resources.files("tutorforum") / "templates")
)


def auth_mech_as_ruby(auth_mech: str) -> str:
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


@FORUM_ENV.add(priority=tutor_hooks.priorities.HIGH)
def _add_base_forum_env(forum_env: dict[str, str]) -> dict[str, str]:
    """
    Add environment variables needed for standard build of forum service.
    """
    forum_env.update(FORUM_ENV_BASE)
    return forum_env


@tutor_hooks.Filters.ENV_PATCHES.add(priority=tutor_hooks.priorities.HIGH)
def _forum_env_patches(patches: list[tuple[str, str]]) -> list[tuple[str, str]]:
    """
    Adds environment variables from FORUM_ENV filter to patches.
    """
    # The forum service is configured entirely via environment variables. Docker
    # Compose and Kubernetes use different syntax to specify environment
    # variables. The following code reads environment variables from the
    # `FORUM_ENV` filter and rendered in the appropriate format for both so they
    # can be included as patches.
    k8s_env_patch = ""
    local_env_patch = ""
    for key, value in FORUM_ENV.apply({}).items():
        # Kubernetes
        k8s_env_patch += f'- name: {key}\n  value: "{value}"\n'
        local_env_patch += f'{key}: "{value}"\n'
    patches += [("forum-k8s-env", k8s_env_patch), ("forum-local-env", local_env_patch)]
    return patches


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
        str(importlib_resources.files("tutorforum") / "patches"),
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
