from glob import glob
import os

from .__about__ import __version__

HERE = os.path.abspath(os.path.dirname(__file__))

templates = os.path.join(HERE, "templates")

config = {
    "add": {
    },
    "defaults": {
        "VERSION": __version__,
        "DOCKER_IMAGE": "{{ DOCKER_REGISTRY }}overhangio/openedx-:{{ TUTOR_VERSION }}",
        "WORKER_DOCKER_IMAGE": "{{ DOCKER_REGISTRY }}overhangio/openedx-ecommerce-worker:{{ ECOMMERCE_VERSION }}",
        "EXTRA_PIP_REQUIREMENTS": [],
        "HOST": "forum.{{ LMS_HOST }}",
        "MONGODB_DATABASE": "cs_comments_service",
        "PORT":"4567",
        "API_KEY":"forumapikey"
    },
}

hooks = {
    "build-image": {
        "fourm": "{{ FOURM_DOCKER_IMAGE }}",
    },
    "init": [],
}


def patches():
    all_patches = {}
    for path in glob(os.path.join(HERE, "patches", "*")):
        with open(path) as patch_file:
            name = os.path.basename(path)
            content = patch_file.read()
            all_patches[name] = content
    return all_patches
