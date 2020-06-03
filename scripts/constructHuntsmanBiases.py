"""
Construct and ingest bias frames for Huntsman.

The bias frames are actually exposure-time matched bias+dark exposures.
"""
import os
import argparse
import subprocess
import datetime
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
    # date = '2018-05-16'
    # date = '2018-08-06'
    date_range = 7
    min_exposures = 1
    datadir = 'DATA'
    calibdir = 'DATA/CALIB'
    rerun = 'processCcdOutputs'
    nodes = 1
    procs = 1
    validity = 1000

    config_file = os.path.join(getPackageDir("obs_huntsman"), "config",
                               "ingestBiases.py")

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
    # TODO: Replace visit with imageId
    metalist = butler.queryMetadata('raw',
                                    ['ccd', 'expTime', 'dateObs', 'visit'],
                                    dataId={'dataType': 'bias'})

    # Select the exposures we are interested in
    exposures = defaultdict(dict)
    for (ccd, exptime, dateobs, imageId) in metalist:

        # Reject exposures outside of date range
        dateobs = parse_date(dateobs)
        if (dateobs < date_start) or (dateobs > date_end):
            continue

        # Update the list of calibs we need
        if exptime not in exposures[ccd].keys():
            exposures[ccd][exptime] = []
        exposures[ccd][exptime].append(imageId)

    # Create the master calibs if we have enough data
    for ccd, exptimes in exposures.items():
        for exptime, image_ids in exptimes.items():

            n_exposures = len(image_ids)

            if n_exposures < min_exposures:
                print(f'Not enough exposures for {exptime}s biases on ccd'
                      f' {ccd} ({n_exposures} of {min_exposures}).')
                continue

            print(f'Making master biases for ccd {ccd} using {n_exposures}'
                  f' exposures of {exptime}s.')

            # Construct the calib for this ccd/exptime combination
            # TODO: Replace visit with imageId
            cmd = f"constructBias.py {datadir} --rerun {rerun}"
            cmd += f" --calib {calibdir}"
            cmd += f" --id visit={'^'.join([f'{id}' for id in image_ids])}"
            cmd += f" expTime={exptime}"
            cmd += f" --nodes {nodes} --procs {procs}"
            cmd += f" --calibId expTime={exptime} calibDate={date}"
            print(f'The command is: {cmd}')
            subprocess.call(cmd, shell=True)

    # Ingest the master calibs
    # TODO: Lookup the correct directory
    print(f"Ingesting master bias frames.")
    cmd = f"ingestCalibs.py {datadir}"
    cmd += f" {datadir}/rerun/{rerun}/calib/bias/{date}/*/*.fits"
    cmd += f" --validity {validity}"
    cmd += f" --calib {calibdir} --mode=link"
    cmd += " --config clobber=True"
    cmd += f" --configfile {config_file}"
    print(f'The ingest command is: {cmd}')
    subprocess.call(cmd, shell=True)
