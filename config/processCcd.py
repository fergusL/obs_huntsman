"""
Subaru-specific overrides for ProcessCcdTask (applied before SuprimeCam- and HSC-specific overrides).
"""

import os

# This was a horrible choice of defaults: only the scaling of the flats
# should determine the relative normalisations of the CCDs!
config.isr.assembleCcd.doRenorm = False

# Cosmic rays and background estimation
config.calibrate.repair.cosmicray.nCrPixelMax = 1000000
config.calibrate.repair.cosmicray.cond3_fac2 = 0.4
config.calibrate.background.binSize = 128
config.calibrate.background.undersampleStyle = 'REDUCE_INTERP_ORDER'
config.calibrate.detection.background.binSize = 128
config.calibrate.detection.background.undersampleStyle='REDUCE_INTERP_ORDER'
config.detection.background.binSize = 128
config.detection.background.undersampleStyle = 'REDUCE_INTERP_ORDER'

# PSF determination
config.calibrate.measurePsf.starSelector.name = 'objectSize'
config.calibrate.measurePsf.starSelector['objectSize'].sourceFluxField = 'base_PsfFlux_flux'
try:
    import lsst.meas.extensions.psfex.psfexPsfDeterminer
    config.calibrate.measurePsf.psfDeterminer["psfex"].spatialOrder = 2
    config.calibrate.measurePsf.psfDeterminer.name = "psfex"
except ImportError as e:
    print "WARNING: Unable to use psfex: %s" % e
    config.calibrate.measurePsf.psfDeterminer.name = "pca"

# Astrometry
from lsst.meas.astrom import AstrometryTask
config.calibrate.astrometry.retarget(AstrometryTask)
config.calibrate.astrometry.refObjLoader.filterMap = {
    'B': 'g',
    'V': 'r',
    'R': 'r',
    'I': 'i',
    'y': 'z',
}

# Reference catalog may not have as good star/galaxy discrimination as our data
config.calibrate.photocal.badFlags += ['base_ClassificationExtendedness_value',]
config.measurement.algorithms['base_ClassificationExtendedness'].fluxRatio = 0.95
# LAM the following had to be set to affect the fluxRatio used in photocal in meas_astrom
config.calibrate.measurement.plugins['base_ClassificationExtendedness'].fluxRatio = 0.95

config.calibrate.photocal.applyColorTerms = True

from lsst.pipe.tasks.setConfigFromEups import setConfigFromEups
menu = { "ps1*": {}, # Defaults are fine
         "sdss*": {"refObjLoader.filterMap": {"y": "z"}}, # No y-band, use z instead
         "2mass*": {"refObjLoader.filterMap": {ff: "J" for ff in "grizy"}}, # No optical bands, use J instead
        }
setConfigFromEups(config.calibrate.photocal, config.calibrate.astrometry, menu)

# Detection
config.detection.isotropicGrow = True
config.detection.returnOriginalFootprints = False

# Measurement
config.doWriteSourceMatches = True

# Activate calibration of measurements: required for aperture corrections
config.calibrate.measurement.load(os.path.join(os.environ['OBS_SUBARU_DIR'], 'config', 'apertures.py'))
# Turn off cmodel until latest fixes (large blends, footprint merging, etc.) are in
# config.calibrate.measurement.load(os.path.join(os.environ['OBS_SUBARU_DIR'], 'config', 'cmodel.py'))
config.calibrate.measurement.load(os.path.join(os.environ['OBS_SUBARU_DIR'], 'config', 'kron.py'))
config.calibrate.measurement.load(os.path.join(os.environ['OBS_SUBARU_DIR'], 'config', 'hsm.py'))
if "shape.hsm.regauss" in config.calibrate.measurement.algorithms:
    config.calibrate.measurement.algorithms["shape.hsm.regauss"].deblendNChild = "" # no deblending has been done

# Activate deep measurements
config.measurement.load(os.path.join(os.environ['OBS_SUBARU_DIR'], 'config', 'apertures.py'))
config.measurement.load(os.path.join(os.environ['OBS_SUBARU_DIR'], 'config', 'kron.py'))
config.measurement.load(os.path.join(os.environ['OBS_SUBARU_DIR'], 'config', 'hsm.py'))
# Note no CModel: it's slow.

# Enable deblender for processCcd
config.measurement.doReplaceWithNoise = True
config.doDeblend = True
config.deblend.maxNumberOfPeaks = 20
config.deblend.load(os.path.join(os.environ['OBS_SUBARU_DIR'], 'config', 'deblend.py'))
config.deblend.maskLimits["NO_DATA"] = 0.25 # Ignore sources that are in the vignetted region

