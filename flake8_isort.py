# -*- coding: utf-8 -*-
from __future__ import print_function
from contextlib import contextmanager
from isort import SortImports

import sys


class DummyFile(object):
    def write(self, x): pass


@contextmanager
def supress_stdout():
    save_stdout = sys.stdout
    sys.stdout = DummyFile()
    yield
    sys.stdout = save_stdout


class Content(object):

    @classmethod
    def read(cls, tree, filename):
        return (
            cls.get_tree_source(tree) or
            cls.get_file_contents(filename) or
            cls.read_stdin())

    @classmethod
    def get_file_contents(cls, filename):
        if filename == 'stdin':
            return None
        with open(filename, 'r') as f:
            return f.read()

    @classmethod
    def get_tree_source(cls, tree):
        return getattr(tree, 'source', None)

    @classmethod
    def read_stdin(cls):
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
        self.content = Content.read(tree, filename)

    def get_line_number(self):
        """Return the line number of the first import.

        Ideally isort would give better feedback so the specific line(s)
        could be identified. This at least will jump past any module docs.

        """
        for lno, line in enumerate(self.content.split('\n'), start=1):
            if line.strip().startswith(('import', 'from')):
                return lno
        return 1

    def run(self):
        with supress_stdout():
            sort_result = SortImports(file_contents=self.content, check=True)
        if sort_result.incorrectly_sorted:
            yield self.get_line_number(), 0, self.message, type(self)
