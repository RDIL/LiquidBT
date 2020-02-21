class DistFormat:
    def __str__(self) -> str:
        return ""


class SourceDist(DistFormat):
    def __str__(self) -> str:
        return "sdist"


class WheelBinaryDist(DistFormat):
    def __str__(self) -> str:
        return "bdist_wheel"


class BuildConfiguration:
    def __init__(self, **kwargs):
        self.pkgname = kwargs["name"]
        self.kwargs = kwargs
        self.data = kwargs.get("data", {})
        self.keepsrc = False
        self._packages = [self]

        assert self.pkgname is not None
        self.setuptools_args = kwargs

        if kwargs.get("keep_generated_sources", False):
            self.setuptools_args.pop("keep_generated_sources")
            self.keepsrc = True

        self.formats = []

    def add_format(self, d):
        if not isinstance(d, DistFormat):
            raise TypeError("Incorrect format specified!")
        self.formats.append(d)

    @property
    def packages(self):
        return self._packages


class BuildPackageSet:
    def __init__(self, **kwargs):
        self.pkgname = ""
        self.kwargs = kwargs
        self.data = kwargs.get("data", {})
        self.packages = []

    def add(self, b: BuildConfiguration):
        if type(b) is not BuildConfiguration:
            raise TypeError(
                "Failed to add a package to the build set, wrong type!"
            )
        self.packages.append(b)

    def remove(self, b: BuildConfiguration):
        if type(b) is not BuildConfiguration:
            raise RuntimeError(
                "Failed to remove a package from the build set, wrong type!"
            )
        self.packages.pop(self.packages.index(b))
