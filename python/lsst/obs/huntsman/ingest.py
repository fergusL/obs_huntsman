"""
This part is responsible for converting FITS headers into appropriate python
objects. The functions defined here are called in ParseTask.getInfoFromMetadata.
See also config.ingest.py.
"""
import re

from lsst.pipe.tasks.ingest import IngestTask, ParseTask, IngestArgumentParser
from lsst.pipe.tasks.ingestCalibs import CalibsParseTask

from huntsman.drp.fitsutil import FitsHeaderTranslatorBase


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


class HuntsmanParseTask(ParseTask, FitsHeaderTranslatorBase):

    def __init__(self, *args, **kwargs):
        FitsHeaderTranslatorBase.__init__(self)
        ParseTask.__init__(self, *args, **kwargs)


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
