import shutil
import os
from .handlers import (
    unsafely_clean,
    setuptools_launch_wrapper,
    create_or_clear,
    write_setup_file,
)
from ..tasks import RunContext


def handle_single_file(ctx: RunContext, file):
    """Runs transformation actions for a single file."""

    # the contents of the source file
    code = open(file, "r").read()

    # clear the file which will hold the transformed code
    handler = open(file.replace(".py", "") + "_dist.py", "w")

    # have the transformers do their thing
    for transformer in ctx.get_build_transformers():
        e = transformer(code)
        if e is not None and type(e) == str:
            code = e
    handler.write(code)
    handler.close()


def handle_package(ctx: RunContext, package):
    """Builds a full package."""

    setuptoolsargs = package.setuptools_args
    pkgname = package.pkgname

    # create all the temp files
    unsafely_clean(pkgname, False)
    create_or_clear("tmpsetup.py")
    shutil.copytree(f"{pkgname}.s", pkgname)
    write_setup_file(ctx, setuptoolsargs, pkgname)

    stringbuilder = ""

    if len(package.formats) < 1:
        raise RuntimeError("No formats specified!")

    for format in package.formats:
        stringbuilder += f" {str(format)}"

    for file in os.listdir(pkgname):
        actualfile = "/".join([pkgname, file])
        code = open(actualfile, "r").read()

        # clear the file
        handler = open(actualfile, "w")
        # have the transformers do their thing
        for transformer in ctx.get_build_transformers():
            e = transformer(code)
            if e is not None and type(e) == str:
                code = e
        handler.write(code)
        handler.close()

    setuptools_launch_wrapper(stringbuilder)

    if os.getenv("DEBUG_NO_CLEAN_ON_END") is None:
        unsafely_clean(pkgname, package.keepsrc)
