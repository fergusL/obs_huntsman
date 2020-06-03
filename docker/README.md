## Tools for running the Huntsman LSST stack with Docker

Ensure that the required environment variables are set:

- `$OBS_HUNTSMAN` should point to the `obs_huntsman` directory.
- `$OBS_HUNTSMAN_TESTDATA` should point to a directory containing "science" and "calib" subdirectories, each containing appropriate FITS images. Note that Docker can't mount symlinks, so they should be actual FITS files.

Then:

```
cd $OBS_HUNTSMAN/docker
docker-compose run lsst_stack
```
### Ingesting images

```
ingestImages.py DATA testdata/science/*.fits --mode=link --calib DATA/CALIB
ingestImages.py DATA testdata/calib/*.fits.fz --mode=link --calib DATA/CALIB
```

Note here that since we are using raw (i.e. not master) calibration files, we use `ingestImages.py` here. If they were master calibration frames, `ingestCalibs.py` should be used instead.

## Create & ingest master calibration frames
```
python $OBS_HUNTSMAN/scripts/constructHuntsmanBiases.py 2018-05-16
python $OBS_HUNTSMAN/scripts/constructHuntsmanBiases.py 2018-08-06
python $OBS_HUNTSMAN/scripts/constructHuntsmanFlats.py 2018-05-16
```

## Process the data
```
processCcd.py DATA --rerun processCcdOutputs --calib DATA/CALIB --id dataType=science
```
