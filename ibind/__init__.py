import logging
import os
import sys
import shutil
from .typeClasses import (
    BuildConfiguration, BuildPackageSet, DistFormat,
    DistInfo, EggBinaryDist, WheelBinaryDist, SourceDist
)

logging.getLogger().setLevel(logging.INFO)

__all__ = [
    "BuildConfiguration", "BuildPackageSet", "DistFormat",
    "DistInfo", "EggBinaryDist", "WheelBinaryDist", "SourceDist",
    "build"
]


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
        pkgname: str = b.pkgname
        logging.getLogger().debug(f"Building package {pkgname}.")
        # create container we can run this in
        open("tmpsetup.py", mode="x")
        shutil.copy(f"{pkgname}.s", pkgname)
        with open("tmpsetup.py", mode="a") as fh:
            fh.write(
                """
                import setuptools
                setuptools.setup(
                """
            )
            for key, value in setuptoolsargs:
                if not key == "packages":
                    fh.write(f"\n    {key}={value},")
                else:
                    fh.write(f"\n    packages=[\"{pkgname}\"]")
            fh.write("\n)")
        stringbuilder: str
        if b.formats == []:
            logging.getLogger().error(f"No formats specified for package {pkgname}!")
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
        os.remove(pkgname)
        try:
            os.remove(f"{b.pkgname}.egg-info")
        except:
            # no egg info
            pass
