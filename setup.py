import setuptools

dependencies = open("requirements.txt", "r").readlines()

setuptools.setup(
    name="liquidbt",
    version="0.1.0",
    description="A modern Python management tool.",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    author="Reece Dunham",
    author_email="me@rdil.rocks",
    packages=setuptools.find_packages(exclude=["unstable", "testpackage"]),
    install_requires=dependencies,
    include_package_data=True,
    zip_safe=False,
)
