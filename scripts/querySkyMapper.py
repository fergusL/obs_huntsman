"""
Script to run a TAP query on the SkyMapper database.
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
from astroquery.utils.tap.core import TapPlus

# Center the query on target
ra0 = 287.4417
dec0 = -63.8575
radius = 4
g_mag_limit = 16
class_star_limit = 0.9

# Define the output file name
output_file = os.path.join(os.environ["OBS_HUNTSMAN_TESTDATA"], "ref_cats",
                           "skymapper_test_raw", "testcat.csv")

# Define the query
query = "SELECT * FROM dr3.master"
query += f" WHERE class_star>{class_star_limit}"
query += f" AND raj2000>{ra0-radius} AND raj2000<{ra0+radius}"
query += f" AND dej2000>{dec0-radius} AND dej2000<{dec0+radius}"
query += f" AND g_psf<{g_mag_limit}"

# Submit the query
skymapper = TapPlus(url="http://api.skymapper.nci.org.au/aus/tap/")
job = skymapper.launch_job_async(query, dump_to_file=True, output_format="csv",
                                 output_file=output_file)

# Make a checkplot
df = pd.read_csv(output_file)
plt.figure()
plt.plot(df["raj2000"], df["dej2000"], "k+", markersize=1)
plt.plot(ra0, dec0, "ro")
plt.show(block=False)
