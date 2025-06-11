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

Upgrading from Redwood (v18)
****************************

In the Sumac release, this plugin was updated to run the new `openedx/forum <https://github.com/openedx/forum>`__ Python application ("v2") instead of the legacy `cs_comments_service <https://github.com/openedx/cs_comments_service>`__ Ruby application ("v1"). See this `deprecation announcement <https://github.com/openedx/cs_comments_service/issues/437>`__ for more information.

For data storage, forum v2 can use either MongoDB or MySQL as a data storage backend:

* New users running Open edX for the first time in Sumac (Tutor v19) will default to the MySQL backend.
* Existing platforms running Redwood or earlier (Tutor < v19) will keep using the MongoDB backend by default.

If you are running an existing platform, you are strongly encouraged to migrate to the new MySQL backend, as the MongoDB backend will disappear in Teak. To do so, you should start by migrating your data::

    tutor local run lms ./manage.py lms forum_migrate_course_from_mongodb_to_mysql --no-toggle all

This command is non-destructive for your data, and can be run multiple times with the same outcome. Once the data migration is successful, you should enable the ``forum_v2.enable_mysql_backend`` global course waffle flag::

    tutor local run lms ./manage.py lms waffle_flag --create --everyone forum_v2.enable_mysql_backend

The forum will then make use of data stored in MySQL instead of MongoDB. Once you are sufficiently confident that the MongoDB data is no longer necessary, you may delete it with::

    tutor local run lms ./manage.py lms forum_delete_course_from_mongodb all

For a more progressive transition, you may decide to migrate data for a single course::

    # removing the no-toggle option will automatically create the course waffle flag just for this course
    tutor local run lms ./manage.py lms forum_migrate_course_from_mongodb_to_mysql <course ID>
    # deleting data is optional and should be done only if you are confident that the migration was successful
    tutor local run lms ./manage.py lms forum_delete_course_from_mongodb <course ID>

For more information, check out the `documentation <https://github.com/openedx/forum>`__ of the forum application.

Breaking Changes
^^^^^^^^^^^^^^^^
As part of the Sumac major release, the following MongoDB-related configuration were removed from this plugin:

* FORUM_MONGODB_DATABASE (default: ``cs_comments_service``)
* FORUM_MONGODB_USE_SSL (default: ``False``)
* FORUM_MONGODB_AUTH_SOURCE (default: ``""``)
* FORUM_MONGODB_AUTH_MECH (default: ``""``)
* FORUM_PORT (default: ``"4567"``)
* FORUM_API_KEY (default: ``"forumapikey"``)
* FORUM_REPOSITORY (default: ``https://github.com/openedx/cs_comments_service.git``)
* FORUM_REPOSITORY_VERSION (default: ``{{ OPENEDX_COMMON_VERSION }}``)

These configurable parameters were deprecated in sumac upgrade when `openedx forum <https://github.com/openedx/forum>`_ was made default in tutor-forum.
Prior to v19 sumac release, if an operator using this plugin had customized the above listed configurations, they will not be able to customize these values with ``tutor config save --set`` after v19 sumac release. To customize the deprecated mongo params, **openedx-common-settings** patch should be used. See below for an example using this patch in a custom plugin:

.. code-block:: python

  tutor_hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-common-settings",  """
           FORUM_MONGODB_DATABASE = 'your_custom_name',
     """
    )
  )


Usage
-----

.. code-block:: bash

    tutor plugins enable forum
    tutor dev|local|k8s launch

Debugging
---------

To debug the forum application, you are encouraged to mount the ``forum`` repository from the host in the development container:

.. code-block:: bash

    tutor mounts add /path/to/forum
    tutor dev launch

Troubleshooting
---------------

This Tutor plugin is maintained by Ghassan Maslamani (ghassan.maslamani@gmail.com).
Community support is available from the official `Open edX forum <https://discuss.openedx.org>`__.
Do you need help with this plugin? See the `troubleshooting <https://docs.tutor.edly.io/troubleshooting.html>`__ section
from the Tutor documentation.

License
-------

This work is licensed under the terms of the `GNU Affero General Public License (AGPL)`_.

.. _GNU Affero General Public License (AGPL): https://github.com/overhangio/tutor-forum/blob/release/LICENSE.txt
