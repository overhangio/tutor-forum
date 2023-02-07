Forum plugin for `Tutor <https://docs.tutor.overhang.io>`__
============================================================

This plugin adds `discussion forums <https://github.com/edx/cs_comments_service>`__ to your `Open edX <https://open.edx.org/>`__ platform, such that students can have conversations about the courses they are following right in your LMS.

.. image:: https://overhang.io/static/catalog/screenshots/forum.png
  :alt: Forum screenshot

Installation
------------

::

    pip install tutor-forum

Usage
-----

::

    tutor plugins enable forum
    tutor local quickstart

Configuration
-------------

- ``FORUM_DOCKER_IMAGE`` (default: ``""{{ DOCKER_REGISTRY }}overhangio/openedx-forum:{{ FORUM_VERSION }}"``)
- ``FORUM_MONGODB_DATABASE`` (default: ``"cs_comments_service"``)
- ``FORUM_PORT`` (default: ``"4567""``)
- ``FORUM_API_KEY`` (default: ``"forumapikey"``)
- ``FORUM_MONGODB_USE_SSL``: (default: ``False``)
- ``FORUM_MONGODB_AUTH_SOURCE``: (default: ``""``)
- ``FORUM_MONGODB_AUTH_MECH``: (default: ``""``)

Caveats for the `mongodb+srv://` syntax
---------------------------------------

While the newer [`mongodb+srv://`](https://www.mongodb.com/developer/products/mongodb/srv-connection-strings/) syntax for the `MONGODB_HOST` is supported, there are some tradeoffs:

- Query paramaters in the URL are not supported. For example, the URL `mongodb+srv://test:test@tutor.local/?ssl=true&authSource=admin` is invalid. Please use the provided configuration options instead.
- The username and password should form part of the URL in the format `mongodb+srv://username:password@host/`.

Debugging
---------

To debug the comments service, you are encouraged to mount the cs_comments_service repo from the host in the development container:

    tutor dev start --mount /path/to/cs_comments_service

Once a local repository is mounted in the image, you will have to install all gems (ruby dependencies)::

    bundle install

License
-------

This software is licensed under the terms of the `AGPLv3 <https://www.gnu.org/licenses/agpl-3.0.en.html>`__.
