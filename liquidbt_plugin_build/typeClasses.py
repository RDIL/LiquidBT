class DistFormat:
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


class BuildConfiguration:
    def __init__(self, name, **kwargs):
        self.pkgname = name
        self.keepsrc = False
        if self.pkgname is None:
            raise Exception(
                """
Error initializing build configuration.
No package name specified!
""")
        self.setuptools_args = kwargs
        if kwargs.get("keep_generated_sources"):
            self.setuptools_args.pop("keep_generated_sources")
            self.keepsrc = True
        self.formats = []

    def add_format(self, d):
        if not isinstance(d, DistFormat):
            raise TypeError("Incorrect format specified!")
        self.formats.append(d)


class BuildPackageSet:
    def __init__(self):
        self.packages = []

    def add(self, b: BuildConfiguration):
        if type(b) is not BuildConfiguration:
            raise TypeError(
                "Failed to add a package to the build set, wrong type!"
            )
        self.packages.append(b)

    def remove(self, b):
        if type(b) is not BuildConfiguration:
            raise RuntimeError(
                "Failed to remove a package from the build set, wrong type!"
            )
        self.packages.pop(self.packages.index(b))
