import ibind
import ibind_plugin_distribute

theset = ibind_plugin_distribute.BuildPackageSet()

config = ibind_plugin_distribute.BuildConfiguration(
    "testpackagerdil",
    author="rdil",
    author_email="me@rdil.rocks",
    url="example.com",
    version="0.0.1"
)
config.add_format(ibind_plugin_distribute.SourceDist())
config.add_format(ibind_plugin_distribute.EggBinaryDist())
config.add_format(ibind_plugin_distribute.WheelBinaryDist())

theset.add(config)

ibind.main(theset, plugins=[
    ibind_plugin_distribute.Distribute()
])
