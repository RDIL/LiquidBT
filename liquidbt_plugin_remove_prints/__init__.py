from liquidbt.plugins import Plugin
import os


class RemovePrints(Plugin):
    """
    Plugin that removes print statements
    from the code that is compiled,
    without changing your source code.

    Note: this can be temporarily disabled
    by setting the environment variable
    "development" to any value (it just
    needs to not be None).
    """

    def load(self, ctx):
        """Loads the plugin."""

        self.ctx = ctx
        self.ctx.add_transformer(self.transform)

    def transform(self, code: str) -> str:
        """Transforms the code."""

        if os.getenv("development") is not None:
            return code
        lines = code.splitlines()
        for line in lines:
            if "print " in line or ("print(" in line and ")" in line):
                lines.pop(lines.index(line))
        return "\n".join(lines)
