from liquidbt.plugins import Plugin
from liquidbt.tasks import create_task
from liquidbt.cli_tools import get_named_command
from os import getenv, system
import sys


class Deploy(Plugin):
    """A plugin for adding a deploy task."""

    twine_args: str

    def __init__(self, twine_args: str):
        """Creates the deploy plugin instance."""
        self.twine_args = twine_args

    def load(self, ctx):
        """Loads the plugin."""
        self.ctx = ctx

        t = create_task("Deploy", self.entrypoint)
        self.ctx.add_task(t)
        if getenv("DEPLOY") is None:
            t.skip()

    def entrypoint(self):
        system(f"{sys.executable} -m twine upload dist/* {self.twine_args}")


def use_env() -> str:
    """Use environment variables for username and password."""

    return f"--username {getenv('TWINE_USERNAME')} --password {getenv('TWINE_PASSWORD')}"
