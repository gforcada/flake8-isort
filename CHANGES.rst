.. -*- coding: utf-8 -*-

Changelog
=========

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
