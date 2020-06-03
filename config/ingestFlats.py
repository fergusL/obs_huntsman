import os.path
from lsst.utils import getPackageDir

configDir = os.path.join(getPackageDir("obs_huntsman"), "config")
config.load(os.path.join(configDir, "ingestCalibs.py"))

config.parse.translators = {'filter': 'translate_filter',
                            'ccd': 'translate_ccd',
                            'calibDate': 'translate_calibDate'}

config.register.columns = {'filter': 'text',
                           'ccd': 'int',
                           'calibDate': 'text',
                           'validStart': 'text',
                           'validEnd': 'text',
                           }

config.register.tables = ['flat', 'bias']
config.register.unique = ['filter', 'ccd', 'calibDate']
config.register.detector = ['filter', 'ccd']
