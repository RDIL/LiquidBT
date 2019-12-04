import os


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
        for key in setuptoolsargs:
            if not key == "packages":
                fh.write(f"\n    {key}=\"{setuptoolsargs[key]}\",")
            else:
                fh.write(f"\n    packages=[\"{pkgname}\"],")
        fh.write("\n)")
