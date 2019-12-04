import os
import sys
import shutil


def create_or_clear(file):
    try:
        open(file, mode="w")
    except FileExistsError:
        os.remove(file)


def write_setup_file(setuptoolsargs, pkgname):
    with open("tmpsetup.py", mode="a") as fh:
        fh.write("""
import setuptools
setuptools.setup("""
        )
        fh.write(f"\n    name=\"{pkgname}\",")
        for key in setuptoolsargs:
            if not key == "packages":
                fh.write(f"\n    {key}=\"{setuptoolsargs[key]}\",")
            else:
                fh.write(f"\n    packages=[\"{pkgname}\"],")
        fh.write("\n)")


def log(message, phase=2, max=6):
    print(f"[{phase}/{max}] {message}")


def setuptools_launch_wrapper(setuptools_args: str):
    """Launches setuptools with the given arguments."""

    setuptools_args = f" --quiet{setuptools_args}"
    if "nt" in sys.platform.lower():
        os.system(f"python tmpsetup.py{setuptools_args}")
    else:
        os.system(f"python3 tmpsetup.py{setuptools_args}")


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
