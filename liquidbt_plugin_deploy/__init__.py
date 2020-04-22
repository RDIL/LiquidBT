from liquidbt.plugins import Plugin
from liquidbt.tasks import create_task, RunContext
from os import getenv, system
import sys


class Deploy(Plugin):
    """A plugin for adding a deploy task."""

    twine_args: str
    ctx: RunContext

    def __init__(self, twine_args: str):
        """Creates the deploy plugin instance."""
        self.twine_args = twine_args

    def load(self, ctx):
        """Loads the plugin."""
        self.ctx = ctx

        if self.ctx.command in ["deploy", "release"]:
            self.ctx.add_task(create_task("Deploy", self.entrypoint))

    def entrypoint(self):
        system(f"{sys.executable} -m twine upload dist/* {self.twine_args}")


def use_env() -> str:
    """Use environment variables for username and password."""

    return "--username {} --password {}".format(
        getenv("TWINE_USERNAME"), getenv("TWINE_PASSWORD")
    )
