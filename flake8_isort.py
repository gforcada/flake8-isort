# -*- coding: utf-8 -*-
from isort import SortImports


class Flake8Isort(object):
    name = 'flake8_isort'
    version = '0.1'
    message = 'I001 found unsorted imports'

    def __init__(self, tree, filename):
        self.filename = filename

    def run(self):
        sort_result = SortImports(self.filename, check=True)
        if sort_result.incorrectly_sorted:
            yield 0, 0, self.message, type(self)
