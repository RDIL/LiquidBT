from liquidbt.plugins import Plugin, TransformerPlugin
from requests import get
import gzip
import tarfile
import shutil
import random


class Package:
    def __init__(self, name, url):
        self.name = name
        self.url = url


class Shade(Plugin):
    def shade(self, bps):
        """Runtime."""
        for package in bps.b.data["shade_packages"]:
            tarname = f"{package.name}.tar"

            open(tarname, mode="wb").write(
                gzip.decompress(
                    get(package.url).content
                )
            )

            tarfile.TarFile(tarname).extractall(package.name)

            # copy the contents to the package
            name_of_shade = f"lib{package.name}{random.randint(100, 100000)}"

            shutil.copytree(
                package.name,
                name_of_shade
            )

            _create_transformer(self.bp, {
                "old": package.name,
                "new": name_of_shade
            })


def _create_transformer(bp, textdata):
    t = TransformerPlugin()

    def process_code(self, code: str):
        return code.replace(textdata["old"], textdata["new"])

    t.process_code = process_code

    bp.use_transformer(t)
