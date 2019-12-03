import logging


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
        if self.pkgname is None:
            raise Exception("Error initializing build configuration - no package name specified!")
        self.setuptools_args = kwargs
        self.formats = []

    def add_format(self, d: DistFormat):
        if (
            type(d) is not DistFormat and
            type(d) is not WheelBinaryDist and
            type(d) is not SourceDist and
            type(d) is not EggBinaryDist and
            type(d) is not DistInfo
        ):
            logging.getLogger().error(
                "Incorrect format specified!"
            )
            return
        self.formats.append(d)


class BuildPackageSet:
    def __init__(self):
        self.packages = []

    def add(self, b: BuildConfiguration):
        if type(b) is not BuildConfiguration:
            logging.getLogger().error("Failed to add a package to the build set, not instance of BuildConfiguration!")
            return
        self.packages.append(b)

    def remove(self, b):
        if type(b) is not BuildConfiguration and type(b) is not int:
            logging.getLogger().error(
                "Failed to remove a package from the build set, not instance of BuildConfiguration or int!"
            )
            return
        if type(b) is int:
            self.packages.pop(b)
        else:
            self.packages.pop(self.packages.index(b))
