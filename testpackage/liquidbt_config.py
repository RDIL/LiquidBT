import liquidbt
from liquidbt_plugin_build import (
    BuildConfiguration, BuildPackageSet, SourceDist,
    WheelBinaryDist, Build
)
from liquidbt_plugin_remove_comments import RemoveComments
from liquidbt_plugin_shade import Shade, BuildPluginBridge, Package

theset = BuildPackageSet()

config = BuildConfiguration(
    "testpackagerdil",
    author="rdil",
    author_email="me@rdil.rocks",
    url="example.com",
    version="0.0.1"
)
config.add_format(SourceDist())
config.add_format(WheelBinaryDist())

theset.add(config)

bp = Build(theset)
bridge = BuildPluginBridge(config, bp)

shaded_packages = [
    Package(
        "slots",
        "https://rdil.mycloudrepo.io/public/repositories/cakebot/slots/slots-1.3.tar.gz",  # noqa
        bridge
    )
]

liquidbt.main(plugins=[
    bp,
    RemoveComments(),
    Shade(bridge, shaded_packages)
])
