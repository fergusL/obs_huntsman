## Tools for running the Huntsman LSST stack with Docker

Ensure that the required environment variables are set:

- `$OBS_HUNTSMAN` should point to the `obs_huntsman` directory.
- `$OBS_HUNTSMAN_TESTDATA` should point to a directory containing "science" and "calib" subdirectories, each containing appropriate FITS images. Note that Docker can't mount symlinks, so they should be actual FITS files.

Then:

```
cd $OBS_HUNTSMAN/docker
docker-compose run lsst_stack
```
### Ingest raw science and calibration images (raw)

```
cd $LSST_HOME
ingestImages.py DATA testdata/science/*.fits --mode=link --calib DATA/CALIB
ingestImages.py DATA testdata/calib/*.fits.fz --mode=link --calib DATA/CALIB
```

Note here that since we are using raw (i.e. not master) calibration files, we use `ingestImages.py` here. If they were master calibration frames, `ingestCalibs.py` should be used instead.

## Create and ingest the astrometry catalogue (refcat)

```
# Prepare the reference catalogue in LSST format
python $OBS_HUNTSMAN/scripts/ingestSkyMapperReference.py

# Move the ingested catalogue into the desired repo's ref_cats directory
cd $LSST_HOME
mkdir DATA/ref_cats
ln -s $LSST_HOME/testdata/ref_cats/skymapper_test/ref_cats/skymapper_dr3 DATA/ref_cats/
```

## Create & ingest master calibration images (biases, flats)
```
python $OBS_HUNTSMAN/scripts/constructHuntsmanBiases.py 2018-05-16
python $OBS_HUNTSMAN/scripts/constructHuntsmanBiases.py 2018-08-06
python $OBS_HUNTSMAN/scripts/constructHuntsmanFlats.py 2018-05-16
```

## Process the data to produce calibrated images (calexps)
```
processCcd.py DATA --rerun processCcdOutputs --calib DATA/CALIB --id dataType=science
```

## Make a SkyMap
```
makeDiscreteSkyMap.py DATA --id --rerun processCcdOutputs:coadd
```

## Warp calexps onto the SkyMap
```
makeCoaddTempExp.py DATA --rerun coadd --selectId filter=g2 --id filter=g2 tract=0 patch=0,0^0,1^0,2^1,0^1,1^1,2^2,0^2,1^2,2 --config doApplyUberCal=False
```

## Make the coadds
```
assembleCoadd.py DATA --rerun coadd --selectId filter=g2 --id filter=g2 tract=0 patch=0,0^0,1^0,2^1,0^1,1^1,2^2,0^2,1^2,2
```
