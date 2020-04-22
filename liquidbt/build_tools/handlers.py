"""Utilities."""

import os
import sys
import shutil
from ..tasks import RunContext
from tostring import tostring


def create_or_clear(file: str):
    """
    Creates a file if it doesn't already exist,
    otherwise clears any existing content from it.
    """

    try:
        open(file, mode="w")
    except FileExistsError:
        os.remove(file)


def write_setup_file(ctx: RunContext, setuptoolsargs, pkgname: str):
    """Writes the setup file."""

    ctx.log("Writing setuptools confguration for " + pkgname)

    with open("tmpsetup.py", mode="a") as fh:
        # start off with basic data
        fh.write("import setuptools\nsetuptools.setup(\n")
        fh.write(f'\n    name="{pkgname}",')

        # these options are required
        setuptoolsargs["zip_safe"] = False
        setuptoolsargs["include_package_data"] = True

        for key in setuptoolsargs:
            val = setuptoolsargs[key]
            if type(val) == list or type(val) == dict or type(val) == bool:
                # doesn't need string inclosing after the =
                fh.write(f"\n    {key}={tostring(val)},")
            else:
                # does need string inclosing after the =
                fh.write(f'\n    {key}="{tostring(val)}",')

        # write the final metadata
        fh.write(f'\n    packages=["{pkgname}"]')
        fh.write("\n)")


def setuptools_launch_wrapper(setuptools_args: str):
    """Launch setuptools with the given arguments."""

    os.system(f"{sys.executable} tmpsetup.py --quiet{setuptools_args}")


def unsafely_clean(pkgname: str, keepsrc: bool):
    """Cleans up the files left behind for the named package."""

    try:
        os.remove("tmpsetup.py")
    except FileNotFoundError:
        pass
    if not keepsrc:
        try:
            shutil.rmtree(pkgname)
        except Exception:
            pass
    try:
        shutil.rmtree(f"{pkgname}.egg-info")
    except Exception:
        pass
