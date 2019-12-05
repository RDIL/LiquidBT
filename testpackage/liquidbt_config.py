import liquidbt
from liquidbt_plugin_build import (
    BuildConfiguration, BuildPackageSet, SourceDist,
    WheelBinaryDist, Build
)
from liquidbt_plugin_remove_comments import RemoveComments

theset = BuildPackageSet()

config = BuildConfiguration(
    "testpackagerdil",
    author="rdil",
    author_email="me@rdil.rocks",
    url="example.com",
    version="0.0.1",
    keep_generated_sources=True
)
config.add_format(SourceDist())
config.add_format(WheelBinaryDist())

theset.add(config)

liquidbt.main(plugins=[
    Build(theset),
    RemoveComments()
])
