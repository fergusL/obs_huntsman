# Cosmic ray removal
# See: https://github.com/lsst/meas_algorithms/blob/master/src/CR.cc
config.repair.doCosmicRay = True

# This controls the maximum number of allowable CRs in an image
config.repair.cosmicray.nCrPixelMax = 1000000

# Raising this contrast parameter reduces the number of CRs
config.repair.cosmicray.cond3_fac = 10

# Lowering this contrast parameter reduces the number of CRs
config.repair.cosmicray.cond3_fac2 = 0


# PSF settings
# See: https://github.com/lsst/pipe_tasks/blob/master/python/lsst/pipe/tasks/measurePsf.py
config.doMeasurePsf = True

# Increasing this number gives a more accurate PSF estimate
config.psfIterations = 3

# Increasing this number allows more PSF candidates
config.measurePsf.starSelector['objectSize'].widthStdAllowed = 0.5
