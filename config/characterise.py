'''
Override the default characterise config parameters by putting them in here.
e.g.:
config.doWrite = False
'''
# Cosmic ray removal
# See: https://github.com/lsst/meas_algorithms/blob/master/src/CR.cc
config.repair.doCosmicRay = True

# We seem to be getting too many CR detections
# For now we can increase the max number of allowable CRs
config.repair.cosmicray.nCrPixelMax = 1000000

# Raising these numbers reduces the number of CRs
config.repair.cosmicray.cond3_fac = 10
config.repair.cosmicray.cond3_fac2 = 10

# This sets the minimum brightness for a CR.
config.repair.cosmicray.min_DN = 100000

# Sometimes there are no initial source detections, causing errors
# Lowering this number gives more sources for PSF fitting (default 10)
config.detection.includeThresholdMultiplier = 5.0

# Try and get PSF fitting to work
config.psfIterations = 1 #More than this and it fails... not sure why.
