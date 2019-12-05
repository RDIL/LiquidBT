import os
import sys
import shutil
from liquidbt.plugins import log


def create_or_clear(file):
    try:
        open(file, mode="w")
    except FileExistsError:
        os.remove(file)


def write_setup_file(setuptoolsargs, pkgname):
    log(f"Writing setuptools confguration for {pkgname}", phase=3)
    with open("tmpsetup.py", mode="a") as fh:
        fh.write("""
import setuptools
setuptools.setup(
"""
        )
        fh.write(f"\n    name=\"{pkgname}\",")
        setuptoolsargs["zip_safe"] = False
        for key in setuptoolsargs:
            val = setuptoolsargs[key]
            if key != "packages":
                if type(val) == str:
                    fh.write(f"\n    {key}=\"{val}\",")
                elif type(val) == bool:
                    fh.write(f"\n    {key}={str(val)},")
        fh.write(f"\n    packages=[\"{pkgname}\"]")
        fh.write("\n)")


def setuptools_launch_wrapper(setuptools_args: str):
    """Launches setuptools with the given arguments."""

    if "nt" in sys.platform.lower():
        os.system(f"python tmpsetup.py --quiet{setuptools_args}")
    else:
        os.system(f"python3 tmpsetup.py --quiet{setuptools_args}")


def unsafely_clean(pkgname):
    """Forcefully clean up."""
    try:
        os.remove("tmpsetup.py")
    except FileNotFoundError:
        pass
    try:
        shutil.rmtree(pkgname)
    except Exception:
        pass
    try:
        shutil.rmtree(f"{pkgname}.egg-info")
    except Exception:
        pass
