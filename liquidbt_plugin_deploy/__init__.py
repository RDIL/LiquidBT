from liquidbt.plugins import Plugin
import typing
import os
import sys


class Deploy(Plugin):
    def __init__(self, package, repo, **kwargs):
        self.kwargs = kwargs

    @property
    def commands(self) -> typing.Dict[str, typing.Callable]:
        return {
            "publish": self.entrypoint,
            "deploy": self.entrypoint
        }

    def entrypoint(self, repository, plugins):
        return


def use_environment():
    return (os.getenv("TWINE_USERNAME"), os.getenv("TWINE_PASSWORD"))


class Repository:
    def __init__(self, credentials, **kwargs) -> None:
        self._credentials = credentials
        self.kwargs = kwargs

    @property
    def url(self) -> typing.Union[str, None]:
        return self.kwargs.get("url", "https://upload.pypi.org/legacy/")

    def upload(self):
        repo = f"--repository-url {self.url}"
        creds = f"-u {self._credentials[0]} -p {self._credentials[1]}"
        cmd = "python3" if sys.platform != "nt" else "python"
        os.system(f"{cmd} -m twine upload dist/* {repo} {creds}")
