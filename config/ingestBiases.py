import os.path
from lsst.utils import getPackageDir

configDir = os.path.join(getPackageDir("obs_huntsman"), "config")
config.load(os.path.join(configDir, "ingestCalibs.py"))

config.parse.translators = {'ccd': 'translate_ccd',
                            'calibDate': 'translate_calibDate',
                            'expTime': 'translate_expTime'}

config.register.columns = {'ccd': 'int',
                           'expTime': 'double',
                           'calibDate': 'text',
                           'validStart': 'text',
                           'validEnd': 'text',
                           }

config.register.tables = ['bias']
config.register.unique = ['ccd', 'calibDate', 'expTime']
config.register.detector = ['ccd']
