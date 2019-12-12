from liquidbt.plugins import Plugin
import typing


class Deploy(Plugin):
    def __init__(self, package, repo, **kwargs) -> None:
        self.kwargs = kwargs

    @property
    def commands(self) -> typing.Dict[str, typing.Callable]:
        return {
            "publish": self.entrypoint,
            "deploy": self.entrypoint
        }

    def entrypoint(self, plugins):
        return


class Repository:
    def __init__(self, name, *args, **kwargs) -> None:
        self._name = name
        self.args = args
        self.kwargs = kwargs

    @property
    def name(self) -> typing.Union[str, None]:
        return self._name

    @property
    def url(self) -> typing.Union[str, None]:
        return self.kwargs.get("url", None)
