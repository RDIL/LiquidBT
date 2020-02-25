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
    def __init__(self, **kwargs):
        self.pkgname = kwargs["name"]
        self.kwargs = kwargs
        self.data = kwargs.get("data", {})
        self.keepsrc = False

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
