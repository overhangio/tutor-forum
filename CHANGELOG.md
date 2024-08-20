# Changelog

This file includes a history of past releases. Changes that were not yet added to a release are in the [changelog.d/](./changelog.d) folder.

<!--
⚠️ DO NOT ADD YOUR CHANGES TO THIS FILE! (unless you want to modify existing changelog entries in this file)
Changelog entries are managed by scriv. After you have made some changes to this plugin, create a changelog entry with:

    scriv create

Edit and commit the newly-created file in changelog.d.

If you need to create a new release, create a separate commit just for that. It is important to respect these
instructions, because git commits are used to generate release notes:
  - Modify the version number in `__about__.py`.
  - Collect changelog entries with `scriv collect`
  - The title of the commit should be the same as the new version: "vX.Y.Z".
-->

<!-- scriv-insert-here -->

<a id='changelog-18.1.0'></a>
## v18.1.0 (2024-08-21)

- 💥[Feature] upgrade to Ruby 3.3 (by @ghassanmas).

- [Bugfix] Fix mounting `cs_comments_service` repository at build- and runtime. (by @regisb)

<a id='changelog-18.0.1'></a>
## v18.0.1 (2024-07-26)

- [Bugfix] Fix legacy warnings during Docker build. (by @regisb)
- [Improvement] ignore TLS certificates on dockerize wait (by @gabor-boros)

<a id='changelog-18.0.0'></a>
## v18.0.0 (2024-06-20)

- 💥[Feature] Upgrade to Redwood (by @DawoudSheraz)

<a id='changelog-17.0.1'></a>
## v17.0.1 (2024-06-13)

- [Bugfix] Make plugin compatible with Python 3.12 by removing dependency on `pkg_resources`. (by @regisb)

<a id='changelog-17.0.0'></a>
## v17.0.0 (2023-12-09)

- 💥[Feature] Upgrade to Quince. (by @ghassanmas)

<a id='changelog-16.0.2'></a>
## v16.0.2 (2023-12-08)

- [Improvement] Support arm64 architecture. (by @ghassanmas)
- [Improvement] Added Makefile and test action to repository and formatted code with Black and isort. (by @CodeWithEmad)

<a id='changelog-16.0.1'></a>
## v16.0.1 (2023-10-02)

- [Improvement] Add a scriv-compliant changelog. (by @regisb)

- [Improvement] Introduces the `FORUM_ENV` filter to which any additional forum
  which simplifies management of environment variables for the forum service.
  Additional environment variables can be added to this filter, and existing
  values can be removed as needed by plugins. These are rendered into the new
  `forum-k8s-env` and `forum-local-env` patches for the kubernetes and docker
  configs respectively. (by @xitij2000)

- [Improvement] Add support for get subscribers of a thread https://github.com/openedx/cs_comments_service/pull/415. (by @Ian2012)

