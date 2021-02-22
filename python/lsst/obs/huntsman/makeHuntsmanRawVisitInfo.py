"""
Useful links:
https://github.com/lsst/obs_base/blob/master/python/lsst/obs/base/makeRawVisitInfo.py
https://pipelines.lsst.io/modules/lsst.afw.image/exposure-fits-metadata.html

Possibly useful:
https://jira.lsstcorp.org/browse/DM-19766
"""
from lsst.geom import SpherePoint
from lsst.geom import degrees
from lsst.afw.coord import Observatory
from lsst.afw.image import RotType
from lsst.obs.base import MakeRawVisitInfo

__all__ = ["MakeHuntsmanRawVisitInfo"]

NaN = float("nan")


class MakeHuntsmanRawVisitInfo(MakeRawVisitInfo):
    """Make a VisitInfo from the FITS header of an Huntsman image"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    observatory = Observatory(-17.882*degrees, 28.761*degrees, 2332)  # long, lat, elev

    def setArgDict(self, md, argDict):
        """Set an argument dict for makeVisitInfo and pop associated metadata
        @param[in,out] md metadata, as an lsst.daf.base.PropertyList or PropertySet
        @param[in,out] argdict a dict of arguments

        While a MakeRawVisitInfo file is mandatory for processCcd.py to run, it isn't mandatory
        for it to actually do anything. Hence this one simply contains a pass statement.
        However, it's recommended that you at least include the exposure time from the image header
        and observatory information (for the latter, remember to edit and uncomment the
        "observatory" variable above.)
        """
        argDict["exposureTime"] = self.popFloat(md, 'EXPTIME')
        argDict["observatory"] = self.observatory

        # This is required to create master darks
        argDict['darkTime'] = self.getDarkTime(argDict)

        # This is required by the astrometry code
        argDict["date"] = self.getDateAvg(md=md, exposureTime=argDict["exposureTime"])

        # Boresight information required to create an initial WCS estimate based on camera geometry
        argDict["boresightRaDec"] = SpherePoint(md["RA-MNT"], md["DEC-MNT"], units=degrees)
        argDict["boresightAirmass"] = md["AIRMASS"]
        argDict["boresightRotAngle"] = 0 * degrees
        argDict["rotType"] = RotType.SKY

    def getDateAvg(self, md, exposureTime):
        """
        Return the date in the middle of the exposure.
        """
        dateObs = self.popIsoDate(md, "DATE-OBS")
        return self.offsetDate(dateObs, 0.5*exposureTime)
