from liquidbt.plugins import TransformerPlugin


class RemoveComments(TransformerPlugin):
    """
    Plugin that removes comments from the code that is compiled,
    without changing your source code.

    Note: this only removes comments, not docstrings.
    """
    def process_code(self, code: str) -> str:
        lines = code.splitlines()
        for line in lines:
            if "# " in line:
                lines.pop(lines.index(line))
        return "\n".join(lines)
