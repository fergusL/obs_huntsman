"""
This may be useful:

https://pipelines.lsst.io/modules/lsst.afw.cameraGeom/cameraGeom.html

This is useful:

https://github.com/lsst/obs_lsstSim/blob/86d1dc5cd3953c6b359c3f5e9ab69ae0c075f781/bin.src/makeLsstCameraRepository.py
"""
import os
import numpy as np

import lsst.afw.table as afwTable
import lsst.geom as lsstGeom
from lsst.afw import cameraGeom
from lsst.utils import getPackageDir

# Detector specifications
config_zwo = {'width': 5496, 'height': 3672, 'saturation': 4095, 'gain': 1.145, 'readNoise': 2.4}
config_sbig = {'width': 3352, 'height': 2532, 'saturation': 65535, 'gain': 0.37, 'readNoise': 20.}
config_test = {'width': 100, 'height': 100, 'saturation': 4095, 'gain': 1.145, 'readNoise': 2.4}


def addAmp(ampCatalog, i, readNoise=1, gain=1, width=0, height=0, saturation=1, overscan=0):
    if overscan != 0:
        raise NotImplementedError("Non-zero overscan not yet implemented.")

    amplifier = cameraGeom.Amplifier.Builder()

    bbox = lsstGeom.Box2I(lsstGeom.Point2I(0, 0), lsstGeom.Extent2I(width, height))

    readoutCorner = cameraGeom.ReadoutCorner.LR   # <----------- TODO: check this
    linearityCoeffs = (1.0, np.nan, np.nan, np.nan)
    linearityType = "None"
    rawBBox = lsstGeom.Box2I(lsstGeom.Point2I(0, 0), lsstGeom.Extent2I(width, height))
    rawXYOffset = lsstGeom.Extent2I(0, 0)
    rawDataBBox = lsstGeom.Box2I(lsstGeom.Point2I(0, 0), lsstGeom.Extent2I(width, height))
    rawHorizontalOverscanBBox = lsstGeom.Box2I(lsstGeom.Point2I(0, 0),
                                               lsstGeom.Extent2I(width, height))
    emptyBox = lsstGeom.BoxI()

    amplifier.setRawFlipX(False)
    amplifier.setRawFlipY(False)
    amplifier.setBBox(bbox)
    amplifier.setName(f'{i}')
    amplifier.setGain(gain)
    amplifier.setSaturation(saturation)
    amplifier.setReadNoise(readNoise)
    amplifier.setReadoutCorner(readoutCorner)
    amplifier.setLinearityCoeffs(linearityCoeffs)
    amplifier.setLinearityType(linearityType)
    amplifier.setRawBBox(rawBBox)
    amplifier.setRawXYOffset(rawXYOffset)
    amplifier.setRawDataBBox(rawDataBBox)
    amplifier.setRawHorizontalOverscanBBox(rawHorizontalOverscanBBox)
    amplifier.setRawVerticalOverscanBBox(emptyBox)
    amplifier.setRawPrescanBBox(emptyBox)

    ampCatalog.append(amplifier)


def makeDetector(ccdId, detector_specification):

    ccdName = ccdId+1

    # Add the amplifiers to the CCD
    ampTable = []
    for i in range(1):
        # addAmp(ampTable, i, readout[ccdId-1][i], gain_all[ccdId-1][i])
        addAmp(ampTable, i, **detector_specification)

    # Create detectorTable (can add more than one CCD here later)
    protoTypeSchema = cameraGeom.Amplifier.getRecordSchema()
    detectorTable = afwTable.BaseCatalog(protoTypeSchema)
    for amp in ampTable:
        record = detectorTable.makeRecord()
        tempAmp = amp.finish()
        tempAmp.toRecord(record)
        detectorTable.append(record)

    # Write the detector to file
    fname = os.path.join(getPackageDir("obs_huntsman"), 'camera', f'n{ccdName}_huntsman.fits')
    return detectorTable.writeFits(fname)


if __name__ == "__main__":

    # for i in range(1):
    for i in range(10):
        camera = makeDetector(i, config_zwo)
    for i in range(10, 16):
        camera = makeDetector(i, config_sbig)
    for i in range(16, 18):
        camera = makeDetector(i, config_test)
