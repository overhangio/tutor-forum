Forum plugin for `Tutor <https://docs.tutor.overhang.io>`__
============================================================

.. TODO add some information here

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

- ``FORUM_DOCKER_IMAGE`` (default: ``""{{ DOCKER_REGISTRY }}overhangio/openedx-forum:{{ TUTOR_VERSION }}"``)
- ``FORUM_HOST`` (default: ``"forum.{{ LMS_HOST }}"``)
- ``FORUM_MONGODB_DATABASE`` (default: ``"cs_comments_service"``)
- ``FORUM_PORT`` (default: ``"4567""``)
- ``FORUM_API_KEY`` (default: ``"forumapikey"``)
 
License
-------

This software is licensed under the terms of the `AGPLv3 <https://www.gnu.org/licenses/agpl-3.0.en.html>`__.
