import logging
import os
import sys
import shutil
from .typeClasses import (
    BuildConfiguration, BuildPackageSet, DistFormat,
    DistInfo, EggBinaryDist, WheelBinaryDist, SourceDist
)
from .plugins import Plugin
from .handlers import create_or_clear, write_setup_file

logging.getLogger().setLevel(logging.INFO)

__all__ = [
    "BuildConfiguration", "BuildPackageSet", "DistFormat",
    "DistInfo", "EggBinaryDist", "WheelBinaryDist", "SourceDist",
    "build", "Plugin"
]


def build(b, plugins=[]):
    for plugin in plugins:
        plugin.load()

    if type(b) is not BuildConfiguration and type(b) is not BuildPackageSet:
        raise Exception("Error running build - Incompatible type passed.")

    if type(b) is BuildPackageSet:
        # type is buildpackageset
        for thepackage in b.packages:
            logging.getLogger().debug(f"Building package {thepackage.pkgname}.")
            build(thepackage)
    else:
        # type is BuildConfiguration
        setuptoolsargs: dict = b.setuptools_args
        pkgname: str = b.pkgname
        logging.getLogger().debug(f"Building package {pkgname}.")
        # create container we can run this in
        create_or_clear("tmpsetup.py")
        shutil.copytree(f"{pkgname}.s", pkgname)
        write_setup_file(setuptoolsargs, pkgname)
        stringbuilder = ""
        if b.formats == []:
            logging.getLogger().error(f"No formats specified for package {pkgname}!")
        else:
            for format in b.formats:
                stringbuilder += f" {str(format)}"  # space so setuptools doesnt freak
        for file in os.listdir(pkgname):
            actualfile = f"{pkgname}/{file}"
            code = open(actualfile, "r").read()
            # clear file
            handle = open(actualfile, "w")
            # have the plugins do their thing
            for plugin in plugins:
                code = plugin.process_code(code)
            handle.write(code)
        if not "nt" in sys.platform.lower():
            os.system(f"python3 tmpsetup.py {stringbuilder}")
        else:
            os.system(f"python tmpsetup.py{stringbuilder}")
        # after build completion
        os.remove("tmpsetup.py")
        shutil.rmtree(pkgname)
        try:
            os.remove(f"{b.pkgname}.egg-info")
        except:
            # no egg info
            pass
