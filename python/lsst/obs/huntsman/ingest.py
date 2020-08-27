"""
This part is responsible for converting FITS headers into appropriate python
objects. The functions defined here are called in ParseTask.getInfoFromMetadata.
See also config.ingest.py.
"""
import os
import re
import yaml

from lsst.utils import getPackageDir
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
        """Translate FITS header into dataType: bias, flat or science."""

        if md['IMAGETYP'] == 'Light Frame':
            # The FIELD keyword is set by pocs.observation.field.field_name.
            # For flat fields, this is "Flat Field"
            if md["FIELD"].startswith("Flat Field"):
                dataType = 'flat'
            else:
                dataType = 'science'
        # For Huntsman, we treat all dark frames as biases.
        # The exposure times are used to match biases with science images.
        elif md['IMAGETYP'] == 'Dark Frame':
            dataType = 'bias'
        else:
            raise NotImplementedError(f'IMAGETYP value not recongnised: '
                                      f"{md['IMAGETYP']}")
        return dataType

    def translate_filter(self, md):
        """
        Translate the given filter name to the abstract filter name.
        For Huntsman, we strip of the serial number.
        """
        return "_".join(md["FILTER"].split("_")[:-1])

    def translate_dateObs(self, md):
        """Return the date of observation as a string."""
        return md['DATE-OBS'][:10]

    def translate_visit(self, md):
        """
        Visit should be an integer value to avoid complications.

        For Huntsman purposes, visit should be common to all exposures
        taken simultaneously by the different cameras. This is encoded by the
        time they were observed, provided there is sufficient temporal
        resolution.

        Unique exposures can therefore be identified by visit/ccd pairs.

        Note: There needs to be space in memory for padding of the ccd number
        used in computeExpId.
        """
        date_obs = md['DATE-OBS']  # This is a string
        datestr = ''.join([s for s in date_obs if s.isdigit()])
        assert len(datestr) == 17, "Date string expected to contain 17 numeric characters."
        return int(datestr)

    def translate_ccd(self, md):
        """
        Get a unique integer corresponding to the CCD.
        """
        ccd_name = md["INSTRUME"]
        filename = os.path.join(getPackageDir("obs_huntsman"), "camera",
                                "translate_ccd.yaml")
        with open(filename, "r") as f:
            ccd = int(yaml.safe_load(f)[ccd_name])
        return ccd


class HuntsmanCalibsParseTask(CalibsParseTask):

    def _translateFromCalibId(self, field, md):
        data = md.getScalar("CALIB_ID")
        match = re.search(r".*%s=(\S+)" % field, data)
        return match.groups()[0]

    def translate_expTime(self, md):
        return float(self._translateFromCalibId("expTime", md))

    def translate_ccd(self, md):
        return int(self._translateFromCalibId("ccd", md))

    def translate_filter(self, md):
        return self._translateFromCalibId("filter", md)

    def translate_calibDate(self, md):
        return self._translateFromCalibId("calibDate", md)

    def translate_calibVersion(self, md):
        return self._translateFromCalibId("calibVersion", md)
