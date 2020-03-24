## Tools for running the Huntsman LSST stack with Docker

Ensure that the required environment variables are set:

- `$OBS_HUNTSMAN` should point to the `obs_huntsman` directory.
- `$OBS_HUNTSMAN_TESTDATA` should point to the directory containing the test data (i.e. a directory containing FITS images).

Then:

```
cd $OBS_HUNTSMAN/docker
docker-compose run lsst_stack
```
### Ingesting images

```
ingestImages.py DATA testdata/*.fits.fz --mode=link
```
