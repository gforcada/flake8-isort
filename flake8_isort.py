# -*- coding: utf-8 -*-
from isort import SortImports

import os


class Flake8Isort(object):
    name = 'flake8_isort'
    version = '0.1'
    message = 'I001 found unsorted imports'

    config_file = None

    def __init__(self, tree, filename):
        self.filename = filename

    @classmethod
    def add_options(cls, parser):
        parser.add_option(
            '--no-isort-config',
            action='store_true',
            help='Do not require an .isort.cfg file to be found'
        )
        parser.config_options.append('no-isort-config')

    @classmethod
    def parse_options(cls, options):
        if options.no_isort_config is None:
            cls.config_file = True
        else:
            cls.config_file = False

    def run(self):
        if self.config_file and not self.search_isort_config():
            yield 0, 0, 'I002 no .isort.cfg file found', type(self)
        else:
            sort_result = SortImports(self.filename, check=True)
            if sort_result.incorrectly_sorted:
                yield 0, 0, self.message, type(self)

    def search_isort_config(self):
        """Search for a .isort.cfg all the way up to the root folder"""
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

        return False
