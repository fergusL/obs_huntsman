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

## Create master calibration frames
```
constructDark.py DATA --rerun processCcdOutputs --id dataType="dark" --nodes 1 --procs 1 --calib DATA/CALIB
constructFlat.py DATA --rerun processCcdOutputs --id dataType="flat" --nodes 1 --procs 1 --calib DATA/CALIB
```

## Ingest the master calibration files
```
ingestCalibs.py DATA DATA/rerun/processCcdOutputs/calib/dark/*.fits --validity 1000 --calib DATA/CALIB --mode=link
ingestCalibs.py DATA DATA/rerun/processCcdOutputs/calib/flat/*.fits --validity 1000 --calib DATA/CALIB --mode=link
```

## Process the data
```
processCcd.py DATA --rerun processCcdOutputs --calib DATA/CALIB --id dataType=science
```
