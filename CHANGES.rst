.. -*- coding: utf-8 -*-

Changelog
=========

5.0.0 (2022-10-08)
------------------

- Update dependencies. [gforcada]

- Revamp GitHub actions. [gforcada]

- Drop python 3.6, and add python 3.10. [gforcada]

- Use linters and formatters to keep code sane and beautiful. [gforcada]

4.2.0 (2022-08-04)
------------------

- Fix compatibility with flake8 version 5. [nhymxu]


4.1.2.post0 (2022-07-25)
------------------------

- Release it as a wheel as well. [gforcada]


4.1.2 (2022-07-25)
------------------

- The package no longer depends on ``testfixtures``. 


4.1.1 (2021-10-14)
------------------

- Release py3 only wheels..


4.1.0 (2021-10-14)
------------------

- Support flake8 4.x [g-as]

- Switch from travis-ci to github actions. [g-as]

- Drop python 2.7 support and 3.5 as well [g-as]


4.0.0 (2020-08-11)
------------------

- Nothing changed yet.


4.0.0a0 (2020-08-07)
--------------------

- support isort >= 5 [bnavigator, pkolbus]


3.0.1 (2020-07-08)
------------------

- Work around `FailedToLoadPlugin` exception by requiring `isort` 4.x. Likewise,
  pin the major version of all dependencies, to reduce risk of any future
  incompatibilities.
  [pkolbus]


3.0.0 (2020-04-15)
------------------

- Let `isort` search the configuration, rather than `flake8-isort` try to find it.
  [jnns]

2.9.1 (2020-03-28)
------------------

- Fix flake8 warning.
  [sobolevn]

2.9.0 (2020-03-16)
------------------

- Add ``python3.8`` support.
  [sobolevn]

2.8.0 (2019-12-05)
------------------

- Look for isort configuration on `.flake8` files as well.
  [JohnHBrock]

- Document how to install `flake8-isort` on conda.
  [marcelotrevisani]

- Look for isort configuration on `pyproject.toml` files as well.
  [sanjioh]

2.7.0 (2019-03-19)
------------------

- Improve the README.
  [barbossa]

- Fix isort output when pipes are used.
  [maerteijn]

2.6.0 (2018-12-01)
------------------

- Use pytest to run tests.
  [gforcada]

- New error code I005 isort foundan unexpected missing import.
  [charettes]

- Add ``isort_show_traceback`` option to show verbose multi-line output
  from ``isort``, turned off by default
  [sobolevn]

2.5 (2018-03-15)
----------------

- Now requires isort >= 4.3.0.
  [jleclanche]


2.4 (2018-02-25)
----------------

- Fix input handling with flake8's --stdin-display-name, and simplify it.
  [blueyed]

- Remove flake8-polyfill dependency.  flake8 >= 3.2.1 is required already, and
  stdin is not read directly anymore.
  [blueyed]

2.3 (2017-12-22)
----------------

- Fix typo.
  [paltman]

- Add tox.ini and .editorconfig to config search.
  [cas--]

- Make this plugin compatible with flake8 hook.
  As the hook copies the files out of tree,
  flake8-isort never finds the correct configuration.
  [jaysonsantos]

2.2.2 (2017-08-19)
------------------

- Workaround for isort bug when skipping files.
  [danpalmer]

2.2.1 (2017-05-12)
------------------

- Release as universal wheel.
  [gforcada]

2.2 (2017-03-26)
----------------

- Support flake8 git hook.
  [sergio-alonso]

- Support python 3.6.
  [gforcada]

- Search configuration on home folder.
  [gforcada]

2.1.3 (2016-11-25)
------------------

- Fix yet another corner case.
  [gforcada]

2.1.2 (2016-11-25)
------------------

- Fix another corner case: ignored files.
  [cas--]

2.1.1 (2016-11-25)
------------------

- Fix corner cases of isort: newlines and grouped imports.
  [cas--]

2.1.0 (2016-11-24)
------------------

- Show the exact line and kind of error,
  rather than a generic message.
  [cas--]

2.0.3 (2016-11-22)
------------------

- Update trove classifiers.
  [gforcada]

2.0.2 (2016-11-22)
------------------

- Add flake8 classifier.
  [sigmavirus24]

- Require flake8 3.2.1.
  flake8 series 3.1.x and 3.2.0 where not reporting flake8-isort errors.
  [gforcada]

- Test on pypy and pypy3.
  [gforcada]

- Fix tests and formatting.
  [gforcada]

2.0.1 (2016-09-22)
------------------

- Fix standard input processing.
  [carljm]


2.0 (2016-09-14)
----------------

- Refactor code to handle flake8 version 3.
  [danpalmer]

- Require flake8 version 3.0.
  [gforcada]

1.3 (2016-06-20)
----------------

- Make error messages clearer.
  [do3cc]

- Use either pep8 or pycodestyle (new name for pep8).
  [Maxim Novikov]

- Fix coveralls.
  [gforcada]

1.2 (2016-03-05)
----------------
- Allow stdin processing, this way text editor can pass input to flake8.
  [mjacksonw]

1.1.1 (2016-02-16)
------------------
- Silence isort messages.
  [gforcada]

- Improve wording.
  [gforcada]

1.1 (2016-02-16)
----------------
- Check for isort configuration on setup.cfg as well.
  [plumdog]

1.0 (2015-12-16)
----------------
- Check for an isort configuration file.
  [gforcada]

0.2 (2015-09-14)
----------------
- Fix entry point.
  [gforcada]

0.1.post0 (2015-09-13)
----------------------
- Release wheels as well.
  [gforcada]

0.1 (2015-09-13)
----------------
- Initial release
  [gforcada]

- Add all boilerplate files.
  [gforcada]

- Create the flake8 plugin per se.
  [gforcada]
