from liquidbt.plugins import Plugin, TransformerPlugin
from requests import get
from typing import List
import gzip
import tarfile
import shutil
import random


# bpb stands for build plugin bridge
class BuildPluginBridge:
    def __init__(self, buildplugin, buildconfiguration):
        self.bp = buildplugin
        self.bc = buildconfiguration


class Package:
    def __init__(self, name, url, bpb):
        self.name = name
        self.url = url
        self.bpb = bpb


class Shade(Plugin):
    def __init__(
        self,
        bpb: BuildPluginBridge,
        packages: List[Package] = [],
    ):
        self.packages = packages
        self.bpb = bpb

    def shade(self):
        """Runtime."""
        for package in self.packages:
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
                "/".join([self.bpb.bc.pkgname, name_of_shade])
            )

            create_transformer(self.bpb, {
                "old": package.name,
                "new": name_of_shade
            })


def create_transformer(bpb, textdata):
    assert type(bpb) == BuildPluginBridge
    t = TransformerPlugin()

    def process_code(self, code: str):
        return code.replace(textdata["old"], textdata["new"])

    t.process_code = process_code

    bpb.bp.use_transformer(t)
