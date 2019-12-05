import liquidbt
from liquidbt_plugin_distribute import (
    BuildConfiguration, BuildPackageSet, SourceDist, EggBinaryDist,
    WheelBinaryDist, Distribute
)

theset = BuildPackageSet()

config = BuildConfiguration(
    "testpackagerdil",
    author="rdil",
    author_email="me@rdil.rocks",
    url="example.com",
    version="0.0.1"
)
config.add_format(SourceDist())
config.add_format(EggBinaryDist())
config.add_format(WheelBinaryDist())

theset.add(config)

liquidbt.main(theset, plugins=[
    Distribute()
])
