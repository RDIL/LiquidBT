from liquidbt.plugins import TransformerPlugin
import os


class RemovePrints(TransformerPlugin):
    """
    Plugin that removes print statements
    from the code that is compiled,
    without changing your source code.

    Note: this can be temporarily disabled
    by setting the environment variable
    "development" to any value (it just
    needs to not be None).
    """

    def process_code(self, code: str) -> str:
        if os.getenv("development") is not None:
            return code
        lines = code.splitlines()
        for line in lines:
            if "print " in line or ("print(" in line and ")" in line):
                lines.pop(lines.index(line))
        return "\n".join(lines)
