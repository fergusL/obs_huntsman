'''
Override the default characterise config parameters by putting them in here.
e.g.:
config.doWrite = False
'''
# Cosmic ray removal
# See: https://github.com/lsst/meas_algorithms/blob/master/src/CR.cc
config.repair.doCosmicRay = False

# We seem to be getting too many CR detections
# For now we can increase the max number of allowable CRs
config.repair.cosmicray.nCrPixelMax = 1000000

# Sometimes there are no initial source detections, causing errors
# Lowering this number gives more sources for PSF fitting (default 10)
config.detection.includeThresholdMultiplier = 3.0

# Try and get PSF fitting to work
config.psfIterations = 1 #More than this and it fails... not sure why.
