# -*- coding: utf-8 -*-

import isort


if hasattr(isort, 'api'):  # isort 5
    from contextlib import redirect_stdout
    from difflib import unified_diff
    from io import StringIO
    from pathlib import Path

    import warnings
else:
    from difflib import Differ
    from testfixtures import OutputCapture

__version__ = '4.1.1'


class Flake8IsortBase(object):
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

    show_traceback = False
    stdin_display_name = None
    search_current = True

    def __init__(self, tree, filename, lines):
        self.filename = filename
        self.lines = lines

    @classmethod
    def add_options(cls, parser):

        parser.add_option(
            '--isort-show-traceback',
            action='store_true',
            parse_from_config=True,
            help='Show full traceback with diff from isort'
        )

    @classmethod
    def parse_options(cls, options):
        cls.stdin_display_name = options.stdin_display_name
        cls.show_traceback = options.isort_show_traceback


class Flake8Isort4(Flake8IsortBase):
    """class for isort <5"""

    def run(self):
        if self.filename is not self.stdin_display_name:
            file_path = self.filename
        else:
            file_path = None
        with OutputCapture() as buffer:
            sort_result = isort.SortImports(
                file_path=file_path,
                file_contents=''.join(self.lines),
                check=True,
                show_diff=True,
            )
        traceback = self._format_isort_output(buffer)

        for line_num, message in self.sortimports_linenum_msg(sort_result):
            if self.show_traceback:
                message += traceback
            yield line_num, 0, message, type(self)

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


class Flake8Isort5(Flake8IsortBase):
    """class for isort >=5"""

    def run(self):
        if self.filename is not self.stdin_display_name:
            file_path = Path(self.filename)
            isort_config = isort.settings.Config(
                settings_path=file_path.parent)
        else:
            file_path = None
            isort_config = isort.settings.Config(
                settings_path=Path.cwd())
        input_string = ''.join(self.lines)
        traceback = ''
        isort_changed = False
        input_stream = StringIO(input_string)
        output_stream = StringIO()
        isort_stdout = StringIO()
        try:
            with redirect_stdout(isort_stdout):
                isort_changed = isort.api.sort_stream(
                    input_stream=input_stream,
                    output_stream=output_stream,
                    config=isort_config,
                    file_path=file_path)
        except isort.exceptions.FileSkipped:
            pass
        except isort.exceptions.ISortError as e:
            warnings.warn(e)
        if isort_changed:
            outlines = output_stream.getvalue()
            diff_delta = "".join(unified_diff(
                              input_string.splitlines(keepends=True),
                              outlines.splitlines(keepends=True),
                              fromfile="{}:before".format(self.filename),
                              tofile="{}:after".format(self.filename)))
            traceback = (isort_stdout.getvalue() + "\n" + diff_delta)
            for line_num, message in self.isort_linenum_msg(diff_delta):
                if self.show_traceback:
                    message += traceback
                yield line_num, 0, message, type(self)

    def isort_linenum_msg(self, udiff):
        """Parse unified diff for changes and generate messages

        Args
        ----
        udiff : unified diff delta

        Yields
        ------
        tuple: A tuple of the specific isort line number and message.
        """
        line_num = 0
        additions = []
        moves = []
        for line in udiff.splitlines():
            if line.startswith('@@', 0, 2):
                line_num = int(line[4:].split(' ')[0].split(',')[0])
                continue
            elif not line_num:  # skip lines before first hunk
                continue
            if line.startswith(' ', 0, 1):
                line_num += 1  # Ignore unchanged lines but increment line_num.
            elif line.startswith('-', 0, 1):
                if line.strip() == '-':
                    yield line_num, self.isort_blank_unexp
                    line_num += 1
                else:
                    moves.append(line[1:])
                    yield line_num, self.isort_unsorted
                    line_num += 1
            elif line.startswith('+', 0, 1):
                if line.strip() == '+':
                    # Include newline additions but do not increment line_num.
                    yield line_num, self.isort_blank_req
                else:
                    additions.append((line_num, line))

        # return all additions that did not move
        for line_num, line in additions:
            if not line[1:] in moves:
                yield line_num, self.isort_add_unexp


Flake8Isort = Flake8Isort5 if hasattr(isort, 'api') else Flake8Isort4
