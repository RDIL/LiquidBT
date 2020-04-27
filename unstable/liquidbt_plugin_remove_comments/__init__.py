from liquidbt.plugins import Plugin
from string import ascii_letters


class RemoveComments(Plugin):
    """
    Plugin that removes comments from the code that is compiled,
    without changing your source code.

    Note: this only removes comments, not docstrings.
    """

    def process_code(self, code: str) -> str:
        lines = code.splitlines()
        for line in lines:
            if "# " in line and line_is_only_comment(line):
                lines.pop(lines.index(line))
        return "\n".join(lines)


def line_is_only_comment(line: str) -> bool:
    for char in line:
        if char in ascii_letters:
            return False
    return True
