""" Script to create the FITS tables describing each camera, located in the camera directory.
Useful links:
https://pipelines.lsst.io/modules/lsst.afw.cameraGeom/cameraGeom.html
https://github.com/lsst/obs_lsstSim/blob/86d1dc5cd3953c6b359c3f5e9ab69ae0c075f781/bin.src/makeLsstCameraRepository.py
"""
import os
import numpy as np

import lsst.afw.table as afwTable
import lsst.geom as lsstGeom
from lsst.afw import cameraGeom
from lsst.utils import getPackageDir

from huntsman.drp.lsst.utils.camera import get_camera_configs


def make_amplifier(camera_name, read_noise, gain, width, height, saturation, overscan, **kwargs):
    """ Make an "amplifier" object. In LSST, a single detector can be comprised of multiple
    amplifiers. This is not the case for Huntsman.
    """
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
    amplifier.setName(camera_name)
    amplifier.setGain(gain)
    amplifier.setSaturation(saturation)
    amplifier.setReadNoise(read_noise)
    amplifier.setReadoutCorner(readoutCorner)
    amplifier.setLinearityCoeffs(linearityCoeffs)
    amplifier.setLinearityType(linearityType)
    amplifier.setRawBBox(rawBBox)
    amplifier.setRawXYOffset(rawXYOffset)
    amplifier.setRawDataBBox(rawDataBBox)
    amplifier.setRawHorizontalOverscanBBox(rawHorizontalOverscanBBox)
    amplifier.setRawVerticalOverscanBBox(emptyBox)
    amplifier.setRawPrescanBBox(emptyBox)

    return amplifier


def make_camera(camera_name, **kwargs):
    """ Make a camera (a detectorTable object), which can in principle contain multiple amplifiers.
    Huntsman's cameras only have one amplifier per camera.
    """
    amplifier = make_amplifier(camera_name=camera_name, **kwargs)

    # Create detectorTable (can add more than one CCD here later)
    protoTypeSchema = cameraGeom.Amplifier.getRecordSchema()
    detectorTable = afwTable.BaseCatalog(protoTypeSchema)

    record = detectorTable.makeRecord()
    tempAmp = amplifier.finish()
    tempAmp.toRecord(record)
    detectorTable.append(record)

    # Write the detector to file
    fname = os.path.join(getPackageDir("obs_huntsman"), 'camera', f'{camera_name}.fits')
    return detectorTable.writeFits(fname)


if __name__ == "__main__":

    for camera_config in get_camera_configs():
        make_camera(**camera_config)
