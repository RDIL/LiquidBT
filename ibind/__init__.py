import setuptools
import logging

logging.getLogger().setLevel(logging.INFO)


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


class BuildConfiguration:
    def __init__(self, **kwargs):
        self.pkgname = kwargs.get("name")
        if self.pkgname is None:
            raise Exception("Error initializing build configuration - no package name specified!")
        self.setuptools_args = kwargs


def build(b):
    if type(b) is not BuildConfiguration and type(b) is not BuildPackageSet:
        raise Exception("Error running build - Incompatible type passed.")

    if type(b) is BuildPackageSet:
        for thepackage in b.packages:
            logging.getLogger().debug(f"Building package {thepackage.get("name")}.")
            setuptools.setup(thepackage.setuptools_args)
    else:
        logging.getLogger().debug(f"Building package {b.get("name")}.")
        setuptools.setup(b.setuptools_args)
