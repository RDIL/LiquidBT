import setuptools
from random import randint

setuptools.setup(
    name="ibin-d",
    version="0.0.".join(str(randint(1, 100000000))),
    packages=setuptools.find_packages()
)