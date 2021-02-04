# Cosmic ray removal
# See: https://github.com/lsst/meas_algorithms/blob/master/src/CR.cc
config.repair.doCosmicRay = False

# This controls the maximum number of allowable CRs in an image
config.repair.cosmicray.nCrPixelMax = 1000000

# Raising this contrast parameter reduces the number of CRs
config.repair.cosmicray.cond3_fac = 10

# Lowering this contrast parameter reduces the number of CRs
config.repair.cosmicray.cond3_fac2 = 0


config.detection.includeThresholdMultiplier = 1


# measurePsf config
config.doMeasurePsf = True
config.measurePsf.starSelector['objectSize'].doFluxLimit = False
config.measurePsf.starSelector['objectSize'].doSignalToNoiseLimit = True
config.measurePsf.starSelector['objectSize'].signalToNoiseMin = 10
config.measurePsf.starSelector['objectSize'].signalToNoiseMax = 50
