# -*- coding: utf-8 -*-
from difflib import Differ
from isort import SortImports
from os.path import expanduser
from testfixtures import OutputCapture

import os


try:
    from configparser import ConfigParser as SafeConfigParser
except ImportError:
    from ConfigParser import SafeConfigParser


__version__ = '2.9.1'


class Flake8Isort(object):
    name = 'flake8_isort'
    version = __version__
    isort_unsorted = (
        'I001 isort found an import in the wrong position'
    )
    no_config_msg = (
        'I002 no configuration found (.isort.cfg or [isort] in configs)'
    )
    isort_blank_req = (
        'I003 isort expected 1 blank line in imports, found 0'
    )
    isort_blank_unexp = (
        'I004 isort found an unexpected blank line in imports'
    )
    isort_add_unexp = (
        'I005 isort found an unexpected missing import'
    )

    config_file = None
    show_traceback = False
    stdin_display_name = None
    search_current = True

    def __init__(self, tree, filename, lines):
        self.filename = filename
        self.lines = lines

    @classmethod
    def add_options(cls, parser):
        parser.add_option(
            '--no-isort-config',
            action='store_true',
            parse_from_config=True,
            help='Do not require explicit configuration to be found'
        )

        parser.add_option(
            '--isort-show-traceback',
            action='store_true',
            parse_from_config=True,
            help='Show full traceback with diff from isort'
        )

    @classmethod
    def parse_options(cls, options):
        if options.no_isort_config is None:
            cls.config_file = True
        else:
            cls.config_file = False

        cls.stdin_display_name = options.stdin_display_name
        cls.show_traceback = options.isort_show_traceback

    def run(self):
        settings_file = self.search_isort_config()
        if self.config_file and not settings_file:
            yield 0, 0, self.no_config_msg, type(self)
        else:
            if self.filename is not self.stdin_display_name:
                file_path = self.filename
            else:
                file_path = None
            with OutputCapture() as buffer:
                sort_result = SortImports(
                    file_path=file_path,
                    file_contents=''.join(self.lines),
                    check=True,
                    settings_path=settings_file,
                    show_diff=True,
                )
            traceback = self._format_isort_output(buffer)

            for line_num, message in self.sortimports_linenum_msg(sort_result):
                if self.show_traceback:
                    message += traceback
                yield line_num, 0, message, type(self)

    def search_isort_config(self):
        # type: () -> Optional[str]  # noqa: F821
        """Search for isort configuration all the way up to the root folder

        Looks for ``.isort.cfg``, ``.editorconfig`` or ``[isort]`` section in
        ``setup.cfg``, ``tox.ini``, or ``.flake8`` config files.
        """
        full_path = os.path.abspath(self.filename)
        split_path = (os.path.dirname(full_path), True)
        while split_path[1]:
            config_on_file = self._search_config_on_path(split_path[0])
            if config_on_file:
                return config_on_file
            split_path = os.path.split(split_path[0])

        if self.search_current:
            return self.search_isort_config_at_current()

        # last attempt, check home folder
        home = expanduser('~')
        config_on_home = self._search_config_on_path(home)
        if config_on_home:
            return config_on_home

        return None

    def search_isort_config_at_current(self):
        # type: () -> Optional[str]  # noqa: F821
        """Search for isort configuration at current directory"""
        return self._search_config_on_path(os.path.realpath('.'))

    def _search_config_on_path(self, path):
        # type: (str) -> Optional[str]  # noqa: F821
        """Search for isort configuration files at the specifed path.

        Args:
            path: The path to search for config files on.

        Return:
            str: the isort config if found otherwise, None
        """
        for config_file in ('.isort.cfg', '.editorconfig'):
            config_file_path = os.path.join(path, config_file)
            if os.path.isfile(config_file_path):
                return config_file_path

        # Check for '[isort]' section in other configuration files.
        for config_file in ('tox.ini', 'setup.cfg', '.flake8'):
            config_file_path = os.path.join(path, config_file)
            config = SafeConfigParser()
            config.read(config_file_path)
            if 'isort' in config.sections():
                return config_file_path

        return None

    def sortimports_linenum_msg(self, sort_result):
        """Parses isort.SortImports for line number changes and message

        Uses a diff.Differ comparison of SortImport `in_lines`:`out_lines` to
        yield the line numbers of import lines that have been moved or blank
        lines added.

        Args:
            sort_imports (isort.SortImports): The isorts results object.

        Yields:
            tuple: A tuple of the specific isort line number and message.
        """
        if sort_result.skipped:
            return

        self._fixup_sortimports_wrapped(sort_result)
        self._fixup_sortimports_eof(sort_result)

        differ = Differ()
        diff = differ.compare(sort_result.in_lines, sort_result.out_lines)

        line_num = 0
        additions = {
            '+ {}'.format(add_import) for add_import in sort_result.add_imports
        }
        for line in diff:
            if line.startswith('  ', 0, 2):
                line_num += 1  # Ignore unchanged lines but increment line_num.
            elif line.startswith('- ', 0, 2):
                line_num += 1
                if line.strip() == '-':
                    yield line_num, self.isort_blank_unexp
                else:
                    yield line_num, self.isort_unsorted
            elif line.strip() == '+':
                # Include newline additions but do not increment line_num.
                yield line_num + 1, self.isort_blank_req
            elif line.strip() in additions:
                yield line_num + 1, self.isort_add_unexp

    def _format_isort_output(self, isort_buffer):
        filtering_out = ('+++', '---', '@@', 'ERROR:')

        valid_lines = ['']
        valid_lines += [
            line
            for line in isort_buffer.output.getvalue().splitlines()
            if line.strip().split(' ', 1)[0] not in filtering_out
        ]

        # Normalizing newlines:
        if len(valid_lines) > 1:
            valid_lines.insert(1, '')
        valid_lines.append('')

        return '\n'.join(valid_lines)

    @staticmethod
    def _fixup_sortimports_eof(sort_imports):
        """Ensure single end-of-file newline in `isort.SortImports.in_lines`

        isort fixes EOF blank lines but this change should be suppressed as
        Flake8 will also flag them.

        Args:
            sort_imports (isort.SortImports): The isorts results object.

        Returns:
            isort.SortImports: The modified isort results object.
        """
        to_remove = {''} | set(sort_imports.add_imports)
        for line in reversed(sort_imports.in_lines):
            if line.strip() in to_remove:
                # If single empty line in in_lines, do nothing.
                if len(sort_imports.in_lines) > 1:
                    sort_imports.in_lines.pop()
            else:
                sort_imports.in_lines.append('')
                break

    @staticmethod
    def _fixup_sortimports_wrapped(sort_imports):
        """Split-up wrapped imports newlines in `SortImports.out_lines`

        isort combines wrapped lines into a single list entry string in
        `out_lines` whereas `in_lines` are separate strings so for diff
        comparison these need to be comparable.

        Args:
            sort_imports (isort.SortImports): The isorts results object.

        Returns:
            isort.SortImports: The modified isort results object.
        """
        for idx, line in enumerate(sort_imports.out_lines):
            if '\n' in line:
                for new_idx, new_line in enumerate(
                        sort_imports.out_lines.pop(idx).splitlines()):
                    sort_imports.out_lines.insert(idx + new_idx, new_line)
