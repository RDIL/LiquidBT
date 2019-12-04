import ibind

theset = ibind.BuildPackageSet()

config = ibind.BuildConfiguration(
    "testpackagerdil",
    author="rdil",
    packages=None,
    version="0.0.1"
)
config.add_format(ibind.SourceDist())

theset.add(config)

ibind.build(theset, plugins=None)
