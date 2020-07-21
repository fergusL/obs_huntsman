import os
import glob
from lsst.utils import getPackageDir
from lsst.meas.algorithms import IngestIndexedReferenceTask as ingestTask


# Specify the repository
# This repo itself doesn't matter: it can be any valid butler repository.
# It just provides something for the Butler to construct itself with.
rootdir = os.environ["LSST_HOME"]
repo = os.path.join(rootdir, "DATA")

# Specify the directories
refcatdir =  os.path.join(rootdir, "testdata", "ref_cats")
input_glob = os.path.join(refcatdir, "skymapper_test_raw", "*.csv")
output_dir = os.path.join(refcatdir, "skymapper_test")

# These lines generate the list of files and do the work:
files = glob.glob(input_glob)
files.sort()

# Load the config file
pkgdir = getPackageDir("obs_huntsman")
configFile = os.path.join(pkgdir, "config", "ingestSkyMapperReference.py")
config = ingestTask.ConfigClass()
config.load(configFile)

# Replace `*files` with e.g. `*files[:10]` to only ingest the first 10
# files, and then run `test_ingested_reference_catalog.py` on the output
# with a glob pattern that matches the first 10 files to check that the
# ingest worked.
args = [repo, "--output", output_dir, *files]
ingestTask.parseAndRun(args=args, config=config)
