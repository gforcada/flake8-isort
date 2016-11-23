# -*- coding: utf-8 -*-
from flake8_polyfill import stdin
from isort import SortImports
from testfixtures import OutputCapture

import os
import pycodestyle


try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser


stdin.monkey_patch('pycodestyle')


class Flake8Isort(object):
    name = 'flake8_isort'
    version = '2.0.3'
    isort_error_msg = (
        'I001 isort found deviations to configured sorting rules, '
        'run it on the file to fix this.'
    )
    no_config_msg = (
        'I002 no configuration found (.isort.cfg or [isort] on setup.cfg)'
    )

    config_file = None

    def __init__(self, tree, filename):
        self.filename = filename

    @classmethod
    def add_options(cls, parser):
        parser.add_option(
            '--no-isort-config',
            action='store_true',
            parse_from_config=True,
            help='Do not require explicit configuration to be found'
        )

    @classmethod
    def parse_options(cls, options):
        if options.no_isort_config is None:
            cls.config_file = True
        else:
            cls.config_file = False

    def run(self):
        if self.config_file and not self.search_isort_config():
            yield 0, 0, self.no_config_msg, type(self)
        else:
            with OutputCapture():
                if self.filename == 'stdin':
                    sort_result = SortImports(
                        file_contents=pycodestyle.stdin_get_value(),
                        check=True,
                    )
                else:
                    sort_result = SortImports(self.filename, check=True)
            if sort_result.incorrectly_sorted:
                yield 0, 0, self.isort_error_msg, type(self)

    def search_isort_config(self):
        """Search for isort configuration all the way up to the root folder

        Either on ``.isort.cfg`` file or an ``[isort]`` section on
        ``setup.cfg``.
        """
        full_path = os.path.abspath(self.filename)
        path_parts = full_path.split(os.path.sep)
        dirs_missing = len(path_parts)

        while dirs_missing > 0:
            dirs_missing -= 1
            partial_parts = path_parts[:dirs_missing]
            partial_path = os.sep.join(partial_parts)

            isort_file = '{0}{1}.isort.cfg'.format(partial_path, os.sep)
            if os.path.exists(isort_file):
                return True

            # If the setup file exists and has an "isort" section,
            # then we've found the configuration.
            setup_file = '{0}{1}setup.cfg'.format(partial_path, os.sep)
            if os.path.exists(setup_file):
                config = ConfigParser()
                config.read(setup_file)
                if 'isort' in config.sections():
                    return True

        return False
