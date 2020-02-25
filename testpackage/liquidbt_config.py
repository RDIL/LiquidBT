import liquidbt
from liquidbt_plugin_build import (
    PackageConfig, SourceDist, WheelBinaryDist, Build
)
from liquidbt_plugin_remove_comments import RemoveComments
from liquidbt_plugin_command_clean import CleanCommand

config = PackageConfig(
    name="testpackagerdil",
    author="rdil",
    author_email="me@rdil.rocks",
    url="https://example.com",
    version="0.0.1"
)
config.add_format(SourceDist())
config.add_format(WheelBinaryDist())

bp = Build([config])

liquidbt.main(plugins=[
    bp,
    RemoveComments(),
    CleanCommand()
])
