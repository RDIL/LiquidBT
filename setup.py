import setuptools

dependencies = open("requirements.txt", "r").readlines()

setuptools.setup(
    name="liquidbt",
    version="0.1.0",
    packages=setuptools.find_packages(exclude=["unstable"]),
    install_requires=dependencies,
    include_package_data=True,
    zip_safe=False
)
