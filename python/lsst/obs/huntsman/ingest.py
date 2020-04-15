"""
This part is responsible for converting FITS headers into appropriate python
objects. The functions defined here are called in ParseTask.getInfoFromMetadata.
See also config.ingest.py.
"""
import re
import numpy as np

from lsst.pipe.tasks.ingest import IngestTask, ParseTask, IngestArgumentParser
from lsst.pipe.tasks.ingestCalibs import CalibsParseTask


class HuntsmanIngestArgumentParser(IngestArgumentParser):

    def _parseDirectories(self, namespace):
        """Don't do any 'rerun' hacking: we want the raw data to end up in the
        root directory"""
        namespace.input = namespace.rawInput
        namespace.output = namespace.rawOutput
        namespace.calib = namespace.rawCalib
        del namespace.rawInput
        del namespace.rawCalib
        del namespace.rawOutput
        del namespace.rawRerun


class HuntsmanIngestTask(IngestTask):
    ArgumentParser = HuntsmanIngestArgumentParser


class HuntsmanParseTask(ParseTask):

    def translate_dataType(self, md):
        '''
        This is by no means a good way of doing things, but is a temporary
        solution for playing with the test data.
        '''
        if md['IMAGETYP'] == 'Light Frame':
            if 'Dither' not in md['FIELD']:
                dataType = 'science'
            else:
                dataType = 'flat'
        elif md['IMAGETYP'] == 'Dark Frame':
            if True:
                dataType = 'dark'
            else:
                dataType = 'bias'
        else:
            raise NotImplementedError(f'IMAGETYPE not recongnised: '
                                      f"{md['IMAGETYP']}")
        return dataType

    def translate_visit(self, md):
        '''
        Return integer value corresponding to visit number.

        This is currently a placeholder.
        '''
        return np.random.randint(0, 1E+6)

    def translate_pointing(self, md):
        '''
        Return integer value corresponding to pointing number.

        This is currently a placeholder.
        '''
        return 0

    def translate_dateObs(self, md):
        '''
        Return a string corresponding to the data type.

        This is currently a placeholder.
        '''
        return md['DATE-OBS'][:10]

    def translate_ccd(self, md):
        '''
        Return an integer corresponding to the ccd.

        This is currently a placeholder.
        '''
        # There should be a matching camera entry
        return 1

                                      
class HuntsmanCalibsParseTask(CalibsParseTask):

    def _translateFromCalibId(self, field, md):
        data = md.getScalar("CALIB_ID")
        match = re.search(r".*%s=(\S+)" % field, data)
        return match.groups()[0]

    def translate_ccd(self, md):
        return int(self._translateFromCalibId("ccd", md))

    def translate_filter(self, md):
        return self._translateFromCalibId("filter", md)

    def translate_calibDate(self, md):
        return self._translateFromCalibId("calibDate", md)

    def translate_calibVersion(self, md):
        return self._translateFromCalibId("calibVersion", md)
