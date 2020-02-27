import liquidbt
from liquidbt_plugin_build import (
    PackageConfig, SourceDist, WheelBinaryDist, Build
)
from liquidbt_plugin_remove_comments import RemoveComments
from liquidbt_plugin_command_clean import CleanCommand

testpackagerdil = PackageConfig(
    name="testpackagerdil",
    author="rdil",
    author_email="me@rdil.rocks",
    url="https://example.com",
    version="0.0.1"
)
testpackagerdil.add_format(SourceDist())
testpackagerdil.add_format(WheelBinaryDist())

bp = Build(
    packages=[testpackagerdil],
    files=["testfile.py"]
)

liquidbt.main(plugins=[
    bp,
    RemoveComments(),
    CleanCommand()
])
