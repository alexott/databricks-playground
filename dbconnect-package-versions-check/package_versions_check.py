from pyspark.sql.types import StringType, MapType
from pyspark.sql.functions import udf, col
from pyspark.sql import SparkSession

import pkg_resources

def get_pkgs(dummy):
    pkgs = dict([(i.key, i.version) for i in pkg_resources.working_set])
    return pkgs

spark = SparkSession.builder.appName("Packages Checker").getOrCreate()

pudf = udf(get_pkgs, MapType(StringType(), StringType()))

remote_pkgs = spark.range(1, 2).select(pudf(col("id"))).first()[0]

local_pkgs = dict([(i.key, i.version) for i in pkg_resources.working_set])

ignored_pkgs = {'setuptools', 'pip', 'wheel'}
# set to True to output the libraries that are installed on executors, but not on driver
report_not_installed = False
# TODO: instead of direct printing, collect into array of dicts, and output at the end
for pkg, ver in remote_pkgs.items():
    if pkg in ignored_pkgs:
        continue
    loc_ver = local_pkgs.get(pkg)
    if loc_ver is not None:
        if ver != loc_ver:
            print(f"Version mismatch for packate {pkg}! Remote: {ver}, Local: {loc_ver}")
    elif report_not_installed:
        print(f"Package {pkg} is not installed locally. Remote version is {ver}")
