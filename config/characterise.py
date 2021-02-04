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


# PSF settings
# See: https://github.com/lsst/pipe_tasks/blob/master/python/lsst/pipe/tasks/measurePsf.py
# See: http://doxygen.lsst.codes/stack/doxygen/x_masterDoxyDoc/object_size_star_selector_8py_source.html
# See: http://doxygen.lsst.codes/stack/doxygen/x_masterDoxyDoc/pca_psf_determiner_8py_source.html
# https://community.lsst.org/t/no-psf-candidates-survive/4400
config.doMeasurePsf = True

# config.measurePsf.doFluxLimit = False
config.measurePsf.starSelector['objectSize'].doSignalToNoiseLimit = True
config.measurePsf.starSelector['objectSize'].doFluxLimit = False
config.measurePsf.starSelector['objectSize'].signalToNoiseMin = 10  # Default 20


config.measurePsf.reserve.fraction = 0.2
config.measurePsf.starSelector["objectSize"].sourceFluxField = 'base_PsfFlux_instFlux'


# Increasing this number gives a more accurate PSF estimate
# config.psfIterations = 3

# Increasing this number allows more PSF candidates
# config.measurePsf.starSelector['objectSize'].widthStdAllowed = 0.5
