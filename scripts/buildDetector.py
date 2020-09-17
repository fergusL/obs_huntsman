"""
This may be useful:

https://pipelines.lsst.io/modules/lsst.afw.cameraGeom/cameraGeom.html

This is useful:

https://github.com/lsst/obs_lsstSim/blob/86d1dc5cd3953c6b359c3f5e9ab69ae0c075f781/bin.src/makeLsstCameraRepository.py
"""
import os
import lsst.afw.table as afwTable
import lsst.afw.geom as afwGeom
import lsst.geom as lsstGeom
from lsst.afw import cameraGeom
from lsst.utils import getPackageDir
import numpy as np


# detector specifications
zwo = {'width': 5496, 'height': 3672, 'saturation': 4095, 'gain': 1.145,
       'readNoise': 2.4}
sbig = {'width': 3352, 'height': 2532, 'saturation': 65535, 'gain': 0.37,
        'readNoise': 20.}

# This is copying from afw/tests/testAmpInfoTable.py:


def addAmp(ampCatalog, i, readNoise=1, gain=1, width=0, height=0, saturation=1):

    amplifier = cameraGeom.Amplifier.Builder()

    os = 0  # pixels of overscan

    bbox = lsstGeom.Box2I(lsstGeom.Point2I(0, 0), lsstGeom.Extent2I(width, height))
    bbox.shift(lsstGeom.Extent2I(width*i,0))

    readoutCorner = cameraGeom.ReadoutCorner.LL if i == 0 else cameraGeom.ReadoutCorner.LR
    linearityCoeffs = (1.0, np.nan, np.nan, np.nan)
    linearityType = "None"
    rawBBox = lsstGeom.Box2I(lsstGeom.Point2I(0, 0), lsstGeom.Extent2I(width,height))
    rawXYOffset = lsstGeom.Extent2I(0, 0)
    rawDataBBox = lsstGeom.Box2I(lsstGeom.Point2I(0 if i==0 else 0, 0), lsstGeom.Extent2I(width,height))
    rawHorizontalOverscanBBox = lsstGeom.Box2I(lsstGeom.Point2I(0 if i==0 else width-os-1, 0), lsstGeom.Extent2I(os, 6220))
    #rawVerticalOverscanBBox = lsstGeom.Box2I(lsstGeom.Point2I(50, 6132), lsstGeom.Extent2I(0, 0))
    #rawPrescanBBox = lsstGeom.Box2I(lsstGeom.Point2I(0, 0), lsstGeom.Extent2I(0, 0))
    emptyBox = lsstGeom.BoxI()

    shiftp = lsstGeom.Extent2I((width)*i,0)
    rawBBox.shift(shiftp)
    rawDataBBox.shift(shiftp)
    rawHorizontalOverscanBBox.shift(shiftp)

    #amplifier.setHasRawInfo(True) #Sets the first Flag=True

    amplifier.setRawFlipX(False)  #Sets the second Flag=False
    amplifier.setRawFlipY(False)  #Sets the third Flag=False
    amplifier.setBBox(bbox)
    amplifier.setName('left' if i == 0 else 'right')
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
    fname = os.path.join(getPackageDir("obs_huntsman"), 'camera',
                                       'n%s_huntsman.fits' % ccdName)
    return detectorTable.writeFits(fname)


if __name__ == "__main__":

    # for i in range(1):
    for i in range(12):
        camera = makeDetector(i, zwo)
    for i in range(12, 18):
        camera = makeDetector(i, sbig)
