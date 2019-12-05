class DistFormat:
    def __init__(self):
        return None

    def __str__(self) -> str:
        return ""


class SourceDist(DistFormat):
    def __str__(self) -> str:
        return "sdist"


class WheelBinaryDist(DistFormat):
    def __str__(self) -> str:
        return "bdist_wheel"


class DistInfo(DistFormat):
    def __str__(self) -> str:
        return "dist_info"


class EggBinaryDist(DistFormat):
    def __str__(self) -> str:
        return "bdist_egg"


class BuildConfiguration:
    def __init__(self, name, **kwargs):
        self.pkgname = name
        self.keepsrc = False
        if self.pkgname is None:
            raise Exception("Error initializing build configuration - no package name specified!")
        self.setuptools_args = kwargs
        if kwargs.get("keep_generated_sources"):
            self.setuptools_args.pop("keep_generated_sources")
            self.keepsrc = True
        self.formats = []

    def add_format(self, d: DistFormat):
        if (
            type(d) is not DistFormat and
            type(d) is not WheelBinaryDist and
            type(d) is not SourceDist and
            type(d) is not EggBinaryDist and
            type(d) is not DistInfo
        ):
            raise TypeError("Incorrect format specified!")
        self.formats.append(d)


class BuildPackageSet:
    def __init__(self):
        self.packages = []

    def add(self, b: BuildConfiguration):
        if type(b) is not BuildConfiguration:
            raise TypeError(
                "Failed to add a package to the build set, not instance of BuildConfiguration!"
            )
        self.packages.append(b)

    def remove(self, b):
        if type(b) is not BuildConfiguration:
            raise RuntimeError(
                "Failed to remove a package from the build set, not BuildConfiguration!"
            )
        self.packages.pop(self.packages.index(b))
