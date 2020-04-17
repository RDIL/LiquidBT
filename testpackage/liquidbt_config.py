import liquidbt
from liquidbt_plugin_remove_prints import RemovePrints
from liquidbt_plugin_command_clean import CleanCommand

testpackagerdil = liquidbt.PackageConfig(
    name="testpackagerdil",
    author="rdil",
    author_email="me@rdil.rocks",
    url="https://example.com",
    version="0.0.1",
    formats=[liquidbt.SourceDist(), liquidbt.WheelBinaryDist()],
)

liquidbt.main(
    plugins=[RemovePrints(), CleanCommand()],
    packages=[testpackagerdil],
    files=["testfile.py"],
)
