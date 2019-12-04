import os
import sys
import shutil
from .typeClasses import (
    BuildConfiguration, BuildPackageSet, DistFormat,
    DistInfo, EggBinaryDist, WheelBinaryDist, SourceDist
)
from .plugins import Plugin
from .handlers import (
    create_or_clear, write_setup_file, log,
    setuptools_launch_wrapper, unsafely_clean
)

__all__ = [
    "BuildConfiguration", "BuildPackageSet", "DistFormat",
    "DistInfo", "EggBinaryDist", "WheelBinaryDist", "SourceDist",
    "build", "Plugin", "log"
]


def actions(b, plugins):
    setuptoolsargs: dict = b.setuptools_args
    pkgname: str = b.pkgname
    # create container we can run this in
    unsafely_clean(pkgname)
    create_or_clear("tmpsetup.py")
    shutil.copytree(f"{pkgname}.s", pkgname)
    write_setup_file(setuptoolsargs, pkgname)
    stringbuilder = ""
    if b.formats == []:
        raise RuntimeError(f"No formats specified for package {pkgname}!")
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
            e = plugin.process_code(code)
            if e is not None and type(e) == str:
                code = e
            del e
        handle.write(code)
    log("Launching setuptools", phase=4)
    setuptools_launch_wrapper(stringbuilder)
    log("Cleaning up", phase=5)
    unsafely_clean(pkgname)
    log("Done!", phase=6)


def build(b, plugins=[]):
    log("Loading Plugins", phase=1)
    if plugins is None:
        plugins = []

    for plugin in plugins:
        plugin.load()

    if type(b) is BuildPackageSet:
        for thepackage in b.packages:
            log(f"Building {thepackage.pkgname}")
            actions(thepackage, plugins)
    elif type(b) is BuildConfiguration:
        log(f"Building {b.pkgname}")
        actions(b, plugins)
    else:
        raise Exception("Error running build - Incompatible type passed.")
    
    for plugin in plugins:
        plugin.shutdown()
