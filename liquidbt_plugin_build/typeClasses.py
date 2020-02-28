from typing import List


class DistFormat:
    def __str__(self) -> str:
        return ""


class SourceDist(DistFormat):
    def __str__(self) -> str:
        return "sdist"


class WheelBinaryDist(DistFormat):
    def __str__(self) -> str:
        return "bdist_wheel"


class PackageConfig:
    pkgname: str
    formats: List[DistFormat]
    setuptools_args: dict

    def __init__(self, **kwargs):
        self.pkgname = kwargs["name"]
        self.kwargs = kwargs
        self.keepsrc = False
        self.formats = kwargs.get("formats", [])

        assert self.pkgname is not None

        if kwargs.get("keep_generated_sources", False):
            self.keepsrc = True

        self.setuptools_args = self._iter_args(kwargs)

    def add_format(self, d):
        if not isinstance(d, DistFormat):
            raise TypeError("Incorrect format specified!")
        self.formats.append(d)

    def _internal_only_kwargs(self):
        return ["keep_generated_sources", "name", "packages", "formats"]

    def _iter_args(self, args):
        built = {}
        for (key, value) in args.items():
            if key not in self._internal_only_kwargs():
                built[key] = value
        return built
