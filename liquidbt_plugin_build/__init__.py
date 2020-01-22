from liquidbt.plugins import Plugin, log
from .handlers import (
    create_or_clear, unsafely_clean,
    setuptools_launch_wrapper, write_setup_file
)
from .typeClasses import (
    BuildConfiguration, BuildPackageSet, DistFormat,
    DistInfo, WheelBinaryDist, SourceDist
)
import os
import shutil
from typing import Union
import liquidbt_plugin_shade

__all__ = [
    "BuildConfiguration", "BuildPackageSet", "DistFormat",
    "DistInfo", "WheelBinaryDist", "SourceDist", "Build"
]


class Build(Plugin):
    def __init__(
        self,
        b: Union[BuildConfiguration, BuildPackageSet],
        *args,
        **kwargs
    ):
        self.b = b
        self.kwargs = kwargs
        self._mant = []  # type: ignore

    @property
    def commands(self):
        return {
            "build": self.entrypoint
        }

    def entrypoint(self, plugins, locale):
        self.plugins = plugins
        self.locale = locale

        if type(self.b) is BuildPackageSet:
            for thepackage in self.b.packages:  # type: ignore
                log(
                    locale["build.building"].format(
                        thepackage.pkgname
                    ),
                    emoji="build"
                )
                self.actions(thepackage)

        elif type(self.b) is BuildConfiguration:
            log(
                locale["build.building"].format(
                    self.b.pkgname  # type: ignore
                ),
                emoji="build"
            )
            self.actions(self.b)

        else:
            raise Exception("Bad type")

    def actions(self, p):
        b = p
        plugins = self.plugins
        locale = self.locale

        setuptoolsargs: dict = b.setuptools_args
        pkgname = b.pkgname
        # create container we can run this in
        unsafely_clean(pkgname, False)
        create_or_clear("tmpsetup.py")
        shutil.copytree(f"{pkgname}.s", pkgname)
        write_setup_file(setuptoolsargs, pkgname)
        for plugin in plugins:
            if type(plugin) == liquidbt_plugin_shade.Shade:
                plugin.shade(self)
        stringbuilder = ""
        if b.formats == []:
            raise RuntimeError()
        else:
            for format in b.formats:
                stringbuilder += f" {str(format)}"
        for file in os.listdir(pkgname):
            actualfile = f"{pkgname}/{file}"
            code = open(actualfile, "r").read()
            # clear file
            handle = open(actualfile, "w")
            # have the plugins do their thing
            log(
                locale["build.transform"],
                phase=4, emoji="transform"
            )
            for plugin in plugins:
                if plugin.plugin_type == "transformer":
                    e = plugin.process_code(code)
                    if e is not None and type(e) == str:
                        code = e
                    del e
            # internal stuff, please ignore
            for plugin in self._mant:
                e = plugin.process_code(code)
                if e is not None and type(e) == str:
                    code = e
                del e
            handle.write(code)
            handle.close()
        log(
            locale["build.launchSetuptools"],
            phase=5, emoji="launch"
        )
        setuptools_launch_wrapper(stringbuilder)
        log(locale["build.clean"], phase=6, emoji="clean")
        unsafely_clean(pkgname, b.keepsrc)
        log(locale["build.done"], phase=7, emoji="done")

    def use_transformer(self, t):
        """
        Manually injects a transformer.
        **Please don't use this.**
        """
        self._mant.append(t)
