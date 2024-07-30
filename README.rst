Forum plugin for `Tutor <https://docs.tutor.edly.io>`__
=======================================================

This plugin adds `discussion forums`_ to your `Open edX`_ platform, such that students
can have conversations about the courses they are following right in your LMS.

.. image:: https://overhang.io/static/catalog/screenshots/forum.png
  :alt: Forum screenshot


.. _discussion forums: https://github.com/openedx/cs_comments_service
.. _Open edX: https://openedx.org/

Installation
------------

.. code-block:: bash

    tutor plugins install forum

Usage
-----

.. code-block:: bash

    tutor plugins enable forum
    tutor dev|local|k8s launch

Configuration
-------------

- ``FORUM_DOCKER_IMAGE`` (default: ``""{{ DOCKER_REGISTRY }}overhangio/openedx-forum:{{ FORUM_VERSION }}"``)
- ``FORUM_MONGODB_DATABASE`` (default: ``"cs_comments_service"``)
- ``FORUM_PORT`` (default: ``"4567""``)
- ``FORUM_API_KEY`` (default: ``"forumapikey"``)
- ``FORUM_MONGODB_USE_SSL``: (default: ``False``)
- ``FORUM_MONGODB_AUTH_SOURCE``: (default: ``""``)
- ``FORUM_MONGODB_AUTH_MECH``: (default: ``""``)
- ``FORUM_REPOSITORY`` (default: ``"https://github.com/openedx/cs_comments_service.git"``)
- ``FORUM_REPOSITORY_VERSION`` (default: ``"{{ OPENEDX_COMMON_VERSION }}"``)

Customising Environment Variables
---------------------------------

To add, or modify environment variables that are supplied to the forum service,
you can use the ``FORUM_ENV`` hook.

To add or modify an environment variable, update the corresponding entry in the
``FORUM_ENV`` dictionary as follows:

.. code-block:: python

    from tutorforum.hooks import FORUM_ENV

    @FORUM_ENV.add()
    def _add_forum_env_vars(env_vars):
        env_vars.update({ "NEW_ENV_VAR": "VALUE" })
        return env_vars

If the environment variable already exists, it will be overridden, otherwise it
will be added. Note that if multiple plugins override the same value, the last
override will apply.

It is possible to use templates when setting the above values.


Caveats for the ``mongodb+srv://`` syntax
-----------------------------------------

While the newer `mongodb+srv:// <https://www.mongodb.com/developer/products/mongodb/srv-connection-strings/>`__ syntax
for the ``MONGODB_HOST`` is supported, there are some tradeoffs:

- Query parameters in the URL will be ignored by the forum. Please use the provided configuration options instead.
- The username and password should form part of the URL in the format ``mongodb+srv://username:password@host/``.

Debugging
---------

To debug the comments service, you are encouraged to mount the ``cs_comments_service`` repo from the host in the development container:

.. code-block:: bash

    tutor mounts add /path/to/cs_comments_service
    tutor dev launch

If the list of dependencies ``Gemfile`` are modified, it is necessary to re-install all `gems`_ (ruby dependencies):

.. code-block:: bash

    tutor dev run forum bundle install

.. _gems: https://guides.rubygems.org/what-is-a-gem/

Troubleshooting
---------------

This Tutor plugin is maintained by Ghassan Maslamani from `Abstract-Technology <https://abstract-technology.de>`__.
Community support is available from the official `Open edX forum <https://discuss.openedx.org>`__.
Do you need help with this plugin? See the `troubleshooting <https://docs.tutor.edly.io/troubleshooting.html>`__ section
from the Tutor documentation.

License
-------

This software is licensed under the terms of the `AGPLv3 <https://www.gnu.org/licenses/agpl-3.0.en.html>`__.
