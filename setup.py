import setuptools
from random import randint

setuptools.setup(
    name="ibind",
    version="0.0.".join(str(randint(1, 100000000))),
    packages=["ibind", "ibind_plugin_obfuscation"],
    package_dir={"": "packages"}
)
