"""
Useful links:
https://github.com/lsst/obs_base/blob/master/python/lsst/obs/base/makeRawVisitInfo.py
https://pipelines.lsst.io/modules/lsst.afw.image/exposure-fits-metadata.html

Possibly useful:
https://jira.lsstcorp.org/browse/DM-19766
"""
import numpy as np

from lsst.afw.geom import degrees
from lsst.afw.coord import Observatory
from lsst.obs.base import MakeRawVisitInfo

__all__ = ["MakeHuntsmanRawVisitInfo"]

NaN = float("nan")

class MakeHuntsmanRawVisitInfo(MakeRawVisitInfo):
    """Make a VisitInfo from the FITS header of an Huntsman image
    """

    observatory = Observatory(-17.882*degrees, 28.761*degrees, 2332)  # long, lat, elev

    def setArgDict(self, md, argDict):
        """Set an argument dict for makeVisitInfo and pop associated metadata
        @param[in,out] md metadata, as an lsst.daf.base.PropertyList or PropertySet
        @param[in,out] argdict a dict of arguments

        While a Make<>RawVisitInfo file is mandatory for processCcd.py to run, it isn't mandatory for it to actually do anything. Hence this one simply contains a pass statement.
        However, it's recommended that you at least include the exposure time from the image header and observatory information (for the latter, remember to edit and uncomment the "observatory" variable above.)
        """
        argDict["exposureTime"] = self.popFloat(md, 'EXPTIME')
        argDict["observatory"] = self.observatory

        # This is required to create master darks
        # argDict['darkTime'] = self.getDarkTime(argDict)

        # This is required by the astrometry code
        argDict["date"] = self.getDateAvg(md=md, exposureTime=argDict["exposureTime"])

    def getDateAvg(self, md, exposureTime):
        """
        Return the date in the middle of the exposure.
        """
        dateObs = self.popIsoDate(md, "DATE-OBS")
        return self.offsetDate(dateObs, 0.5*exposureTime)
