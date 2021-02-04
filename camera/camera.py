""" Code to load the camera config into the LSST stack.
See:
    https://pipelines.lsst.io/py-api/lsst.afw.cameraGeom.CameraConfig.html
    https://pipelines.lsst.io/py-api/lsst.afw.cameraGeom.DetectorConfig.html
"""
from lsst.afw.cameraGeom.cameraConfig import CameraConfig
from lsst.afw.geom.transformConfig import TransformConfig
from huntsman.drp.lsst.utils.camera import get_camera_configs, get_config


def create_detector_config(camera_config):
    """ Create a `lsst.afw.cameraGeom.cameraConfig.DetectorConfig` object from the camera config.
    Args:
        camera_config (abc.Mapping): The camera config.
    Returns:
        lsst.afw.cameraGeom.cameraConfig.DetectorConfig
    """
    # For some reason we have to do this import here. Thanks, LSST.
    from lsst.afw.cameraGeom.cameraConfig import DetectorConfig

    detector_config = DetectorConfig()
    detector_config.transformDict.nativeSys = 'Pixels'
    detector_config.transposeDetector = False

    # Detector bounding box in pixels
    detector_config.bbox_y0 = 0
    detector_config.bbox_x0 = 0
    detector_config.bbox_y1 = camera_config["height"]
    detector_config.bbox_x1 = camera_config["width"]

    # Name of detector slot
    detector_config.name = camera_config["camera_name"]

    # Pixel size in mm
    detector_config.pixelSize_x = camera_config["pixel_size"]
    detector_config.pixelSize_y = camera_config["pixel_size"]

    # Position of the reference point in the detector in pixels in transposed coordinates
    detector_config.refpos_x = 0.5 * (detector_config.bbox_x1 + detector_config.bbox_x0)
    detector_config.refpos_y = 0.5 * (detector_config.bbox_y1 + detector_config.bbox_y0)

    # Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
    detector_config.detectorType = 0

    # Offsets from the origin of the camera in mm in the transposed system.
    detector_config.offset_x = camera_config.get("offset_x", 0.0)
    detector_config.offset_y = camera_config.get("offset_y", 0.0)

    # 3D position angle of the CCD
    detector_config.yawDeg = camera_config.get("yaw", 0.0)
    detector_config.rollDeg = camera_config.get("roll", 0.0)
    detector_config.pitchDeg = camera_config.get("pitch", 0.0)

    return detector_config


if not isinstance(config, CameraConfig):
    raise TypeError(f"Config is wrong type. Expected , got {type(config)}.")

CONFIG = get_config()
CAMERA_CONFIGS = get_camera_configs(config=CONFIG)

# ==================================================================================================
# Global detector configs

# This isn't strictly required for CameraMapper
config.name = 'Huntsman'

# This defines the native coordinate system:
# FocalPlane is (x, y) in mm (rather than radians or spixels, for example)
config.transformDict.nativeSys = 'FocalPlane'

# Sets the plate scale in arcsec/mm (zwo pix size 0.0024mm and 1.2611"):
config.plateScale = CONFIG["cameras"]["plate_scale"]

# Specify transformation between focal plane units and field angle units.
# This is required by the stack as of v20.
# One of its uses is to calculate the pixel size for the initial WCS.
ZWO_PIXEL_SIZE = CONFIG["cameras"]["presets"]["zwo"]["pixel_size"]
config.transformDict.transforms = {}
config.transformDict.transforms['FieldAngle'] = TransformConfig()
config.transformDict.transforms['FieldAngle'].transform['radial'].coeffs = [0.0, ZWO_PIXEL_SIZE]
config.transformDict.transforms['FieldAngle'].transform.name = 'radial'

# ==================================================================================================
# Camera-specific configs

config.detectorList = {}  # Oh great, detectorList is actually a dict. Thanks again, LSST.

for i, camera_config in enumerate(CAMERA_CONFIGS):

    config.detectorList[i] = create_detector_config(camera_config)

    # Serial string associated with this specific detector
    config.detectorList[i].serial = str(i+1)

    # ID of detector slot
    config.detectorList[i].id = i+1
