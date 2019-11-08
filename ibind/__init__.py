import logging
import os
import sys

logging.getLogger().setLevel(logging.INFO)


class DistFormat:
    def __init__(self) -> None:
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


def build(b):
    if type(b) is not BuildConfiguration and type(b) is not BuildPackageSet:
        raise Exception("Error running build - Incompatible type passed.")

    if type(b) is BuildPackageSet:
        # type is buildpackageset
        for thepackage in b.packages:
            logging.getLogger().debug(f"Building package {thepackage.pkgname}.")
            build(thepackage)  # well yeah its risky but...
    else:
        # type is BuildConfiguration
        setuptoolsargs: dict = b.setuptools_args
        logging.getLogger().debug(f"Building package {b.pkgname}.")
        # create container we can run this in
        try:
            open("tmpsetup.py", mode="x")
        except:
            open("tmpsetup.py", mode="w")
        with open("tmpsetup.py", mode="a") as fh:
            fh.write(
                """
                import setuptools
                setuptools.setup(
                """
            )
            for key, value in setuptoolsargs:
                fh.write(f"\n    {key}={value},")
            fh.write("\n)")
            stringbuilder: str
            if b.formats == []:
                logging.getLogger().error(f"No formats specified for package {b.pkgname}!")
            else:
                for format in b.formats:
                    if stringbuilder == "":
                        stringbuilder = f"{str(format)}"
                    else:
                        stringbuilder += f" {str(format)}"  # space so setuptools doesnt freak
            if not "nt" in sys.platform.lower():
                os.system(f"python3 tmpsetup.py {stringbuilder}")
            else:
                os.system(f"python tmpsetup.py {stringbuilder}")
            # after build completion
            os.remove("tmpsetup.py")
            try:
                os.remove(f"{b.pkgname}.egg-info")
            except:
                # no egg info
                pass
