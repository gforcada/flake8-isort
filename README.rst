.. -*- coding: utf-8 -*-

.. image:: https://travis-ci.org/gforcada/flake8-isort.svg?branch=master
   :target: https://travis-ci.org/gforcada/flake8-isort

.. image:: https://coveralls.io/repos/gforcada/flake8-isort/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/gforcada/flake8-isort?branch=master

Flake8 meet isort
=================
Use `isort`_ to check if the imports on your python files are sorted the way you expect.

Add an ``.isort.cfg`` to define how you want your imports sorted and run flake8 as you usually do.

See `isort documentation`_ for ``.isort.cfg`` available options.

Install
-------
Install with pip::

    $ pip install flake8-isort

Requirements
------------
- Python 2.7, 3.3, 3.4
- flake8
- isort

License
-------
GPL 2.0

.. _`isort`: https://pypi.python.org/pypi/isort
.. _`isort documentation`: https://github.com/timothycrosley/isort/wiki/isort-Settings
