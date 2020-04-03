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
ingestImages.py DATA testdata/science/*.fits --mode=link
ingestImages.py DATA testdata/calib/*.fits.fz --mode=link
```

Note here that since we are using raw (i.e. not master) calibration files, we use `ingestImages.py` here. If they were master calibration frames, `ingestCalibs.py` should be used instead.

## Create master calibration frames
```
constructDark.py DATA --rerun processCcdOutputs --id dataType="dark" --nodes 1 --procs 1 --clobber-config
constructFlat.py DATA --rerun processCcdOutputs --id dataType="flat" --nodes 1 --procs 1 --clobber-config
```

## Ingest the master calibration files
```
TBD.
```

## Process the data
```
processCcd.py DATA --rerun processCcdOutputs --id --calib CALIB --clobber-config
```
