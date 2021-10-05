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

License
-------

This software is licensed under the terms of the `AGPLv3 <https://www.gnu.org/licenses/agpl-3.0.en.html>`__.
