"""
See: https://pipelines.lsst.io/py-api/lsst.afw.cameraGeom.DetectorConfig.html
"""
import lsst.afw.cameraGeom.cameraConfig

assert type(config) is lsst.afw.cameraGeom.cameraConfig.CameraConfig

# This isn't strictly required for CameraMapper
config.name = 'Huntsman'

# Sets the plate scale in arcsec/mm:
# zwo pix size 0.0024mm and 1.2611"
config.plateScale=527.54167

# This defines the native coordinate system:
# FocalPlane is (x,y) in mm (rather than radians or pixels, for example).
config.transformDict.nativeSys = 'FocalPlane'

# For some reason, it must have "Pupil" defined:
config.transformDict.transforms = {}
config.transformDict.transforms['FieldAngle'] = lsst.afw.geom.transformConfig.TransformConfig()

# coeffs = [0,1] is the default. This is only necessary if you want to convert
# between positions on the focal plane.
# config.transformDict.transforms['FieldAngle'].transform['inverted'].transform.retarget(target=lsst.afw.geom.transformRegistry['radial'])
# config.transformDict.transforms['FieldAngle'].transform['inverted'].transform.coeffs=[0.0, 1.0]
# config.transformDict.transforms['FieldAngle'].transform.name='inverted'

# Define a dict of detectors:
config.detectorList = {}

# NB need to update this to get parameters right for ZWO cameras
for i in range(12):
    config.detectorList[i+1] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()

    # y0 of pixel bounding box
    config.detectorList[i+1].bbox_y0=0

    # y1 of pixel bounding box
    config.detectorList[i+1].bbox_y1=3672

    # x1 of pixel bounding box
    config.detectorList[i+1].bbox_x1=5496

    # x0 of pixel bounding box
    config.detectorList[i+1].bbox_x0=0

    # Name of detector slot
    config.detectorList[i+1].name='n'+str(i+1)+'_huntsman'

    # Pixel size in mm
    config.detectorList[i+1].pixelSize_x = 0.0024
    config.detectorList[i+1].pixelSize_y = 0.0024

    # Name of native coordinate system
    config.detectorList[i+1].transformDict.nativeSys='Pixels'

    # x position of the reference point in the detector in pixels in transposed coordinates.
    config.detectorList[i+1].refpos_x = 2748   # Half detector x size in pixels

    # y position of the reference point in the detector in pixels in transposed coordinates.
    config.detectorList[i+1].refpos_y = 1836  # Half detector y size in pixels

    # Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
    config.detectorList[i+1].detectorType = 0

    # Offsets from the origin of the camera in mm in the transposed system.
    config.detectorList[i+1].offset_x = 0.
    config.detectorList[i+1].offset_y = 0.

    # 3D position angle of the CCD
    config.detectorList[i+1].yawDeg = 0.0
    config.detectorList[i+1].rollDeg = 0.0
    config.detectorList[i+1].pitchDeg = 0.0

    # Serial string associated with this specific detector
    config.detectorList[i+1].serial = str(i+1)

    # ID of detector slot
    config.detectorList[i+1].id = i+1

for i in range(12, 18):
    config.detectorList[i+1]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()

    # All non-commented lines ARE REQUIRED for CameraMapper:
    # y0 of pixel bounding box
    config.detectorList[i+1].bbox_y0=0

    # y1 of pixel bounding box
    config.detectorList[i+1].bbox_y1=2532

    # x1 of pixel bounding box
    config.detectorList[i+1].bbox_x1=3352

    # x0 of pixel bounding box
    config.detectorList[i+1].bbox_x0=0

    # Name of detector slot
    config.detectorList[i+1].name='n'+str(i+1)+'_huntsman'

    # Pixel size in mm
    config.detectorList[i+1].pixelSize_x=0.0054
    config.detectorList[i+1].pixelSize_y=0.0054

    # Name of native coordinate system
    config.detectorList[i+1].transformDict.nativeSys='Pixels'

    # x position of the reference point in the detector in pixels in transposed coordinates.
    config.detectorList[i+1].refpos_x = 1676

    # y position of the reference point in the detector in pixels in transposed coordinates.
    config.detectorList[i+1].refpos_y = 1266

    # Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
    config.detectorList[i+1].detectorType=0

    # x offset from the origin of the camera in mm in the transposed system.
    config.detectorList[i+1].offset_x=0.

    # y offset from the origin of the camera in mm in the transposed system.
    config.detectorList[i+1].offset_y=0.

    config.detectorList[i+1].yawDeg=0.0
    config.detectorList[i+1].rollDeg=0.0
    config.detectorList[i+1].pitchDeg=0.0

    # Serial string associated with this specific detector
    config.detectorList[i+1].serial=str(i+1)

    # ID of detector slot
    config.detectorList[i+1].id=i+1
