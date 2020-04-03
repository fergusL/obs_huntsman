"""
This file tells ParseTask.getInfoFromMetadata how to obtain information from the
FITS header. There are two options: One can specify a direct translation
between a FITS header key and a LSST config key, OR you can specify a translator
function (defined in lsst.obs_X.XParseTask) that converts FITS headers into
appropriate Python objects. The latter option takes preference if both are
specified.

LSST stack does implicit conversion of types into those specified in
config.register.columns, so make sure they are correct.

Combinations of the columns specified in config.register.unique must be unique
among files.
"""
from lsst.obs.huntsman.ingest import HuntsmanParseTask

config.parse.retarget(HuntsmanParseTask)

# Specify mappings between FITS keys and LSST config keys
config.parse.translation = {'expTime': 'EXPTIME',
                            #'ccd': 'CAM-ID',   #ccd should be an integer
                            'ccdTemp': 'CCD-TEMP',
                            'expId': 'IMAGEID',
                            'taiObs': 'DATE-OBS', #Not sure what this one is
                            'filter': 'FILTER',
                            'field': 'FIELD'
                            }

# Specify default key value pairs which are used if FITS keyword is missing
config.parse.defaults = {}

# Specify functions to translate meta data to a python object
# They are implemented in lsst.obs_X.XParseTask
config.parse.translators = {'visit': 'translate_visit',
                            'pointing': 'translate_pointing',
                            'dateObs': 'translate_dateObs',
                            'dataType': 'translate_dataType',
                            'ccd': 'translate_ccd'
                            }

# Declare the columns that should be read
config.register.columns = {'field': 'text',
                           'visit': 'int',
                           'ccd': 'int',
                           'pointing': 'int',
                           'filter': 'text',
                           'dateObs': 'text',
                           'taiObs': 'text',
                           'expTime': 'double',
                           'expId': 'text',
                           'dataType': 'text'
                           }

# Define what key combination constitutes a unique observation
config.register.unique = ['visit', 'ccd']

# This is needed for some reason. Not sure what it does yet.
# More info here: https://lsstcamdocs.readthedocs.io/en/latest/ingest.html
config.register.visit = ['visit', 'field', 'filter', 'dateObs', 'taiObs']
