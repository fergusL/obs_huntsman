. $LSST_HOME/loadLSST.bash
eups declare obs_huntsman v1 -r $STACK/obs_huntsman
setup obs_huntsman v1
ingestImages.py DATA testdata/*.fits.fz --mode=link
/bin/bash
