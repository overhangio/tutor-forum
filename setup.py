import io
import os
from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))


def load_readme():
    with io.open(os.path.join(HERE, "README.rst"), "rt", encoding="utf8") as f:
        return f.read()


def load_about():
    about = {}
    with io.open(
        os.path.join(HERE, "tutorforum", "__about__.py"),
        "rt",
        encoding="utf-8",
    ) as f:
        exec(f.read(), about)  # pylint: disable=exec-used
    return about


ABOUT = load_about()


setup(
    name="tutor-forum",
    version=ABOUT["__version__"],
    url="https://github.com/overhangio/tutor-forum",
    project_urls={
        "Code": "https://github.com/overhangio/tutor-forum",
        "Issue tracker": "https://github.com/overhangio/tutor-forum/issues",
        "Community": "https://discuss.openedx.org",
    },
    license="AGPLv3",
    author="Overhang.IO",
    maintainer="Zaat.dev",
    maintainer_email="ghassan@zaat.dev",
    description="forum plugin for Tutor",
    long_description=load_readme(),
    long_description_content_type="text/x-rst",
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=["tutor>=16.0.0,<17.0.0"],
    entry_points={
        "tutor.plugin.v1": [
            "forum = tutorforum.plugin"
        ]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
