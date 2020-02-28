from liquidbt.plugins import Plugin
import os
import sys


class Deploy(Plugin):
    twine_args: str

    def __init__(self, twine_args: str, *args, **kwargs):
        self.kwargs = kwargs
        self.twine_args = twine_args

    @property
    def commands(self):
        return {
            "publish": self.entrypoint,
            "deploy": self.entrypoint
        }

    def entrypoint(self, *args, **kwargs):
        os.system(f"{sys.executable} -m twine upload dist/* {self.twine_args}")


def use_environment() -> str:
    """Use environment variables for username and password."""
    return f"--username {os.getenv('TWINE_USERNAME')} --password {os.getenv('TWINE_PASSWORD')}"
