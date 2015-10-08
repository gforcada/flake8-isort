# -*- coding: utf-8 -*-
from __future__ import print_function
from isort import SortImports

import sys


class Read(object):

    @classmethod
    def file(cls, filename):
        if filename == 'stdin':
            return None
        with open(filename, 'r') as f:
            return f.read()

    @classmethod
    def tree(cls, tree):
        return getattr(tree, 'source', None)

    @classmethod
    def stdin(cls):
        content = sys.stdin.read()
        if not content:
            # issue: https://github.com/PyCQA/pep8/pull/443
            print('Flake8Isort: stdin is empty')
        return content


class Flake8Isort(object):
    name = 'flake8_isort'
    version = '0.1'
    message = 'I001 found unsorted imports'

    def __init__(self, tree, filename, builtins=None):
        self.content = Read.tree(tree) or Read.file(filename) or Read.stdin()

    def run(self):
        sort_result = SortImports(file_contents=self.content, check=True)
        if sort_result.incorrectly_sorted:
            yield 0, 0, self.message, type(self)
