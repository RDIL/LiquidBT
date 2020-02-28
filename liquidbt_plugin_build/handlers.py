"""Utilities."""

import os
import sys
import shutil
import textwrap
from liquidbt.plugins import log, log_continued_message


def create_or_clear(file):
    try:
        open(file, mode="w")
    except FileExistsError:
        os.remove(file)


def write_setup_file(setuptoolsargs, pkgname):
    log_continued_message(
        f"Writing setuptools confguration for {pkgname}"
    )
    with open("tmpsetup.py", mode="a") as fh:
        fh.write(textwrap.dedent("""
            import setuptools
            setuptools.setup(
        """))
        fh.write(f"\n    name=\"{pkgname}\",")
        setuptoolsargs["zip_safe"] = False
        setuptoolsargs["include_package_data"] = True
        for key in setuptoolsargs:
            val = setuptoolsargs[key]
            if type(val) == str:
                fh.write(f"\n    {key}=\"{val}\",")
            elif type(val) == bool:
                fh.write(f"\n    {key}={str(val)},")
            elif type(val) == dict:
                # something like package_data will be a dict
                fh.write("\n    " + key + "={")
                for option in val:
                    fh.write(f"\n        {option}: \"{val[option]}\",")
                fh.write("\n    }")
        fh.write(f"\n    packages=[\"{pkgname}\"]")
        fh.write("\n)")


def setuptools_launch_wrapper(setuptools_args: str):
    """Launch setuptools with the given arguments."""
    os.system(f"{sys.executable} tmpsetup.py --quiet{setuptools_args}")


def unsafely_clean(pkgname, keepsrc):
    """Force clean up."""

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
