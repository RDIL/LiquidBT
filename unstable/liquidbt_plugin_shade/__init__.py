from liquidbt.plugins import Plugin
from liquidbt.tasks import RunContext
from requests import get
import gzip
import tarfile
import shutil


class Shade(Plugin):
    def __init__(self, shaded_packages):
        self.shaded_packages = shaded_packages

    def load(self, ctx):
        self.ctx = ctx

    def shade(self):
        """Runtime."""

        for package in self.shaded_packages:
            tarname = f"{package['name']}.tar"

            open(tarname, mode="wb").write(
                gzip.decompress(get(package.url).content)
            )

            tarfile.TarFile(tarname).extractall(package.name)

            shutil.copytree(package.name, name_of_shade)


def _create_transformer(ctx: RunContext, old_import, new_import):
    """
    Creates a transformer that remaps the value of `old_import` to
    `new_import.`
    """

    ctx.add_transformer(
        lambda code: code.replace(old_import, new_import)
    )
