from liquidbt.plugins import Plugin, TransformerPlugin, log
from .handlers import (
    create_or_clear, unsafely_clean,
    setuptools_launch_wrapper, write_setup_file
)
from .typeClasses import *
import os
import shutil

__all__ = [
    "BuildConfiguration", "BuildPackageSet", "DistFormat",
    "DistInfo", "EggBinaryDist", "WheelBinaryDist", "SourceDist",
    "Build"
]


class Build(Plugin):
    def __init__(self, b):
        self.b = b

    @property
    def commands(self):
        return {
            "build": self.entrypoint
        }

    def entrypoint(self, plugins):
        if type(self.b) is BuildPackageSet:
            for thepackage in self.b.packages:
                log(f"Building {thepackage.pkgname}")
                self.actions(thepackage, plugins)
        elif type(self.b) is BuildConfiguration:
            log(f"Building {self.b.pkgname}")
            self.actions(self.b, plugins)
        else:
            raise Exception("Error running build - Incompatible type passed.")

    @staticmethod
    def actions(b, plugins):
        setuptoolsargs: dict = b.setuptools_args
        pkgname = b.pkgname
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
                if plugin.plugin_type == "transformer":
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