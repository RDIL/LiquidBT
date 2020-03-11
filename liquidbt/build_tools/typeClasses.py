from typing import List


class DistFormat:
    """An abstract distribution format."""

    def __str__(self) -> str:
        return ""


class SourceDist(DistFormat):
    """A source distribution, typically a `.tar.gz`."""

    def __str__(self) -> str:
        return "sdist"


class WheelBinaryDist(DistFormat):
    """A wheel distribution (`.whl` file)."""

    def __str__(self) -> str:
        return "bdist_wheel"


class PackageConfig:
    """The configuration for a single package."""

    pkgname: str
    formats: List[DistFormat]
    setuptools_args: dict

    def __init__(self, **kwargs):
        """Creates the class."""

        self.pkgname = kwargs["name"]
        self.kwargs = kwargs
        self.keepsrc = False
        self.formats = kwargs.get("formats", [])

        assert self.pkgname is not None

        if kwargs.get("keep_generated_sources", False):
            self.keepsrc = True

        self.setuptools_args = self._iter_args(kwargs)

    def add_format(self, d):
        """Adds the passed DistFormat."""
        if not isinstance(d, DistFormat):
            raise TypeError("Incorrect format specified!")
        self.formats.append(d)

    def _internal_only_kwargs(self):
        """
        Keyword arguments that shouldn't make it to setuptools,
        or will be modified before being given to setuptools.
        """
        return ["keep_generated_sources", "name", "packages", "formats"]

    def _iter_args(self, args):
        """
        Filters through the keyword arguments and excludes the ones that we don't want.
        """
        built = {}
        for (key, value) in args.items():
            if key not in self._internal_only_kwargs():
                built[key] = value
        return built
