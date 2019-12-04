import ibind

theset = ibind.BuildPackageSet()

config = ibind.BuildConfiguration(
    "testpackagerdil",
    author="rdil",
    packages=None,
    version="0.0.1"
)
config.add_format(ibind.SourceDist())
config.add_format(ibind.EggBinaryDist())
config.add_format(ibind.WheelBinaryDist())

theset.add(config)

ibind.main(theset, plugins=None)
