import setuptools

dependencies = open("requirements.txt", "r").readlines()

setuptools.setup(
    name="liquidbt",
    version="0.1.0",
    packages=setuptools.find_packages("packages"),
    package_dir={"": "packages"},
    install_requires=dependencies
)
