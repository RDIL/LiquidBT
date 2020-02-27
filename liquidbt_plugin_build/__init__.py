from liquidbt.plugins import Plugin, log, log_continued_message
from .handlers import (
    create_or_clear, unsafely_clean,
    setuptools_launch_wrapper, write_setup_file
)
from .typeClasses import (
    PackageConfig, DistFormat, WheelBinaryDist,
    SourceDist
)
import os
import shutil
from typing import List


__all__ = [
    "PackageConfig", "DistFormat", "WheelBinaryDist",
    "SourceDist", "Build", "_package_list_type",
    "_file_list_type"
]

_package_list_type = List[PackageConfig]
_file_list_type = List[str]


class Build(Plugin):
    packages: _package_list_type
    files: _file_list_type
    kwargs: dict

    def __init__(
        self,
        packages: _package_list_type = [],
        files: List[str] = [],
        *args,
        **kwargs
    ):
        self.packages = packages
        self.kwargs = kwargs
        self.files = files
        self._manual_triggers = []  # type: ignore

    @property
    def commands(self):
        return {
            "build": self.entrypoint
        }

    def entrypoint(self, plugins, locale):
        self.plugins = plugins
        self.locale = locale

        for afile in self.files:
            log(
                locale["build.building"].format(afile),
                emoji="build"
            )
            self.actions_exclusive_to_named_file(afile)
        for thepackage in self.packages:
            log(
                locale["build.building"].format(
                    thepackage.pkgname
                ),
                emoji="build"
            )
            self.actions(thepackage)

    def actions(self, package):
        plugins = self.plugins
        locale = self.locale

        setuptoolsargs: dict = package.setuptools_args
        pkgname = package.pkgname

        # create container we can run this in
        unsafely_clean(pkgname, False)
        create_or_clear("tmpsetup.py")
        shutil.copytree(f"{pkgname}.s", pkgname)
        write_setup_file(setuptoolsargs, pkgname)
        stringbuilder = ""

        if len(package.formats) < 1:
            raise RuntimeError("No formats specified!")

        for format in package.formats:
            stringbuilder += f" {str(format)}"

        for file in os.listdir(pkgname):
            actualfile = f"{pkgname}/{file}"
            code = open(actualfile, "r").read()
            # clear file
            handle = open(actualfile, "w")
            # have the plugins do their thing
            log_continued_message(
                locale["build.transform"]
            )
            for plugin in plugins + self._manual_triggers:
                if plugin.plugin_type == "transformer":
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

        if os.getenv("DEBUG_NO_CLEAN_ON_END") is None:
            log(locale["build.clean"], phase=6, emoji="clean")
            unsafely_clean(pkgname, package.keepsrc)

        log(locale["build.done"], phase=7, emoji="done")

    def actions_exclusive_to_named_file(self, file):
        code = open(file, "r").read()
        # clear file
        handle = open(file.replace(".py", "") + "_dist.py", "w")
        # have the plugins do their thing
        log_continued_message(
            self.locale["build.transform"]
        )
        for plugin in self.plugins:
            if plugin.plugin_type == "transformer":
                e = plugin.process_code(code)
                if e is not None and type(e) == str:
                    code = e
                del e
        handle.write(code)
        handle.close()

    def use_transformer(self, t):
        """
        Manually injects a transformer.
        **Please don't use this unless you know
        what you are doing.**
        """
        self._manual_triggers.append(t)
