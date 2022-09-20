Forum plugin for `Tutor <https://docs.tutor.overhang.io>`__
============================================================

This plugin adds `discussion forums <https://github.com/openedx/cs_comments_service>`__ to your `Open edX <https://openedx.org/>`__ platform, such that students can have conversations about the courses they are following right in your LMS.

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
    tutor local launch 

Configuration
-------------

- ``FORUM_DOCKER_IMAGE`` (default: ``""{{ DOCKER_REGISTRY }}overhangio/openedx-forum:{{ FORUM_VERSION }}"``)
- ``FORUM_MONGODB_DATABASE`` (default: ``"cs_comments_service"``)
- ``FORUM_PORT`` (default: ``"4567""``)
- ``FORUM_API_KEY`` (default: ``"forumapikey"``)

Debugging
---------

To debug the comments service, you are encouraged to mount the cs_comments_service repo from the host in the development container:

    tutor dev start --mount /path/to/cs_comments_service

Once a local repository is mounted in the image, you will have to install all gems (ruby dependencies)::

    bundle install

Troubleshooting
---------------

This Tutor plugin is maintained by Ghassan Maslamani from `Zaat.dev <https://Zaat.dev>`__. Community support is available from the official `Open edX forum <https://discuss.openedx.org>`__. Do you need help with this plugin? See the `troubleshooting <https://docs.tutor.overhang.io/troubleshooting.html>`__ section from the Tutor documentation.


License
-------

This software is licensed under the terms of the `AGPLv3 <https://www.gnu.org/licenses/agpl-3.0.en.html>`__.
