from setuptools import find_packages, setup

__version__ = "0.0.1"

INSTALL_REQUIRES=[]
with open("requirements.txt", "r") as file:
    for l in file:
        l = l.strip()
        if l != "" and l[0] != "#":
            INSTALL_REQUIRES.append(l)

setup(
    name="databricks-pyspark-helpers",
    packages=find_packages(exclude=["tests", "tests.*"]),
    setup_requires=["wheel"],
    install_requires=INSTALL_REQUIRES,
    version=__version__,
    description="Useful PySpark/Databricks functions",
    author="Alex Ott <alexott@gmail.com>"
)
