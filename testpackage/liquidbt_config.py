import liquidbt
from liquidbt_plugin_build import (
    BuildConfiguration, BuildPackageSet, SourceDist,
    WheelBinaryDist, Build
)
from liquidbt_plugin_remove_comments import RemoveComments
from liquidbt_plugin_shade import Shade, Package

theset = BuildPackageSet()

config = BuildConfiguration(
    name="testpackagerdil",
    author="rdil",
    author_email="me@rdil.rocks",
    url="https://example.com",
    version="0.0.1"
)
config.add_format(SourceDist())
config.add_format(WheelBinaryDist())

theset.add(config)

shaded_packages = [
    Package(
        "slots",
        "https://rdil.mycloudrepo.io/public/repositories/cakebot/slots/slots-1.3.tar.gz"  # noqa
    )
]

theset.data["shade_packages"] = shaded_packages

bp = Build(theset)

liquidbt.main(plugins=[
    bp,
    RemoveComments()
])
