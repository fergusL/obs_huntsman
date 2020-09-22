from __future__ import absolute_import, division, print_function
import os

from lsst.daf.persistence import Policy
from lsst.obs.base import CameraMapper
from .makeHuntsmanRawVisitInfo import MakeHuntsmanRawVisitInfo
from .huntsmanFilters import HUNTSMAN_FILTER_DEFINITIONS

import traceback
from lsst.obs.base.utils import createInitialSkyWcs, InitialSkyWcsError


class HuntsmanMapper(CameraMapper):

    packageName = 'obs_huntsman'

    # A rawVisitInfoClass is required by processCcd.py
    MakeRawVisitInfoClass = MakeHuntsmanRawVisitInfo

    # Specify the filter definitions
    filterDefinitions = HUNTSMAN_FILTER_DEFINITIONS

    def __init__(self, inputPolicy=None, **kwargs):

        # Declare the policy file
        policyFile = Policy.defaultPolicyFile(self.packageName, "HuntsmanMapper.yaml", "policy")
        policy = Policy(policyFile)

        # Add policy to the mapper
        super(HuntsmanMapper, self).__init__(policy, os.path.dirname(policyFile), **kwargs)

        # Define filters
        self.filterDefinitions.reset()
        self.filterDefinitions.defineFilters()

        """
        # Define filters
        self.filters = {}

        #Define your set of filters; you can have as many filters as you like...
        afwImageUtils.defineFilter(name='Clear',  lambdaEff=535.5, alias=['Clear'])

        #...add them to your filter dict...
        self.filters['Clear'] = afwImage.Filter('Clear').getCanonicalName()

        #...and set your default filter.
        self.defaultFilterName = 'Clear'
        """

    def _computeCcdExposureId(self, dataId):
        '''
        Every exposure needs a unique ID.
        Here, I construct a unique ID by multiplying the visit number by
        64 to accomodate that we may have up to 64 CCDs exposed for every visit.
        processCcd.py will fail with a NotImplementedError() without this.

        NB:
        Having too large of an expId causes processCcd to fail,
        processCcd FATAL: Failed on dataId={'dataType': 'science', 'dateObs':
            '2018-08-02', 'ccd': 13, 'visit': 20180802100911034, 'expTime':
            300.0}: RuntimeError: expId=1291571334458306189 uses 61 bits >
            expBits=30
        So rather than multiply the visit by the number of ccds, instead just
        append the ccd number to the end of the visit id.
        '''
        pathId = self._transformId(dataId)
        visit = pathId['visit']
        ccd = int(pathId['ccd'])
        visit = int(visit)
        # strip miliseconds and first two digits of year from visit id
        expId = int(str(visit)[2:-3]+str(ccd))
        # I think this is better(?) as it preserves the date/ccd info in expId
        # return visit*64 + ccd
        return expId

    def bypass_ccdExposureId(self, datasetType, pythonType, location, dataId):
        '''You need to tell the stack that it needs to refer to the above _computeCcdExposureId function.
        processCcd.py will fail with an AttributeError without this.
        '''
        return self._computeCcdExposureId(dataId)

    def bypass_ccdExposureId_bits(self, datasetType, pythonType, location, dataId):
        '''You need to tell the stack how many bits to use for the ExposureId. Here I'm say that the ccd ID takes up to 6 bits (2**6=64), and I can have up to 16,777,216 (=2**24) visits in my survey.
        processCcd.py will fail with an AttributeError without this.
        '''
        # return 24+6
        # Note: the visit id is of form yyyymmddhhmmssffff and ccd id is nn
        # the unique expid is formed as concatenation of the two, requiring
        # 61 bits (2**61=2305843009213693952)
        return 46

    def _extractDetectorName(self, dataId):
        '''
        Every detector needs a name.
        Here, I simply use the ccd ID number extracted from the header and recorded via the ingest process.
        processCcd.py will fail with a NotImplementedError() without this.
        '''
        return int("%(ccd)d" % dataId)

    def std_bias(self, item, dataId):
        """Standardize a bias dataset by converting it to an Exposure instead
        of an Image"""
        return self._standardizeExposure(self.exposures['raw'], item, dataId,
                                         trimmed=False, setVisitInfo=False,
                                         filter=False)

    def std_flat(self, item, dataId):
        """Standardize a flat dataset by converting it to an Exposure instead
        of an Image"""
        return self._standardizeExposure(self.exposures['raw'], item, dataId,
                                         trimmed=False, setVisitInfo=False,
                                         filter=True)

    def _createInitialSkyWcs(self, exposure):
        # DECam has a coordinate system flipped on X with respect to our
        # VisitInfo definition of the field angle orientation.
        # We have to override this method until RFC-605 is implemented, to pass
        # `flipX=True` to createInitialSkyWcs below.
        self._createSkyWcsFromMetadata(exposure)

        if exposure.getInfo().getVisitInfo() is None:
            msg = "No VisitInfo; cannot access boresight information. Defaulting to metadata-based SkyWcs."
            self.log.warn(msg)
            return
        try:
            newSkyWcs = createInitialSkyWcs(exposure.getInfo().getVisitInfo(), exposure.getDetector(),
                                            flipX=True)
            exposure.setWcs(newSkyWcs)
        except InitialSkyWcsError as e:
            msg = "Cannot create SkyWcs using VisitInfo and Detector, using metadata-based SkyWcs: %s"
            self.log.warn(msg, e)
            self.log.debug("Exception was: %s", traceback.TracebackException.from_exception(e))
            if e.__context__ is not None:
                self.log.debug("Root-cause Exception was: %s",
                               traceback.TracebackException.from_exception(e.__context__))
