"""
Construct and ingest bias frames for Huntsman.

The bias frames are actually exposure-time matched bias+dark exposures.
"""
import os
import subprocess
import datetime
import argparse
from dateutil.parser import parse as parse_date
from collections import defaultdict

import lsst.daf.persistence as dafPersist
from lsst.utils import getPackageDir

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('date', type=str, help='The calibration date.')
    args = parser.parse_args()
    date = args.date

    # Some placeholder inputs
    date_range = 7
    min_exposures = 1
    datadir = 'DATA'
    calibdir = 'DATA/CALIB'
    rerun = 'processCcdOutputs'
    nodes = 1
    procs = 1
    validity = 1000

    config_file = os.path.join(getPackageDir("obs_huntsman"), "config",
                               "ingestFlats.py")

    # We will create calibs for this date
    date_parsed = parse_date(date)

    # Specify the date range we are interested in
    date_range = datetime.timedelta(days=date_range)
    date_start = date_parsed - date_range
    date_end = date_parsed + date_range

    # Create the Bulter object
    butler = dafPersist.Butler(inputs=os.path.join(os.environ['LSST_HOME'],
                                                   datadir))
    # Query butler for dark exposures
    # TODO: Replace visit with expId
    metalist = butler.queryMetadata('raw',
                                    ['ccd', 'filter', 'dateObs', 'expId'],
                                    dataId={'dataType': 'flat'})

    # Select the exposures we are interested in
    exposures = defaultdict(dict)
    for (ccd, filter, dateobs, expId) in metalist:

        # Reject exposures outside of date range
        dateobs = parse_date(dateobs)
        if (dateobs < date_start) or (dateobs > date_end):
            continue

        # Update the list of calibs we need
        if filter not in exposures[ccd].keys():
            exposures[ccd][filter] = []
        exposures[ccd][filter].append(expId)

    # Create the master calibs if we have enough data
    for ccd, filters in exposures.items():
        for filter, exp_ids in filters.items():

            n_exposures = len(exp_ids)

            if n_exposures < min_exposures:
                print(f'Not enough exposures for flats in {filter} filter on'
                      f' ccd {ccd} ({n_exposures} of {min_exposures}).')
                continue

            print(f'Making master flats for ccd {ccd} using {n_exposures}'
                  f' exposures in {filter} filter.')

            # Construct the calib for this ccd/exptime combination
            cmd = f"constructFlat.py {datadir} --rerun {rerun}"
            cmd += f" --calib {calibdir}"
            cmd += f" --id expId={'^'.join([f'{id}' for id in exp_ids])}"
            cmd += " dataType='flat'"  # TODO: remove
            cmd += f" filter={filter}"
            cmd += f" --nodes {nodes} --procs {procs}"
            cmd += f" --calibId filter={filter} calibDate={date}"
            print(f'The command is: {cmd}')
            subprocess.call(cmd, shell=True)

    # Ingest the master calibs
    # TODO: Lookup the correct directory
    print(f"Ingesting master {filter} filter flats frames for ccd {ccd}.")
    cmd = f"ingestCalibs.py {datadir}"
    cmd += f" {datadir}/rerun/{rerun}/calib/flat/{date}/*/*.fits"
    cmd += f" --validity {validity}"
    cmd += f" --calib {calibdir} --mode=link"
    cmd += " --config clobber=True"
    cmd += f" --configfile {config_file}"
    print(f'The ingest command is: {cmd}')
    subprocess.call(cmd, shell=True)
