import ibind
import ibind_plugin_obfuscation

theset = ibind.BuildPackageSet()

config = ibind.BuildConfiguration(
    "testpackagerdil",
    author="rdil",
    packages=None,
    version="0.0.1"
)
config.add_format(ibind.SourceDist())

theset.add(config)

ibind.build(theset, plugins=[
    ibind_plugin_obfuscation.Plugin()
])
