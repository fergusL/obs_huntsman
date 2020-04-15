from lsst.obs.huntsman.ingest import HuntsmanCalibsParseTask

config.parse.retarget(HuntsmanCalibsParseTask)

config.parse.translators = {'filter': 'translate_filter',
                            'ccd': 'translate_ccd',
                            'calibDate': 'translate_calibDate',
                            }

config.register.columns = {'filter': 'text',
                           'ccd': 'int',
                           'calibDate': 'text',
                           'validStart': 'text',
                           'validEnd': 'text',
                           }

config.register.detector = ['filter', 'ccd']
config.register.unique = ['filter', 'ccd', 'calibDate']
config.register.tables = ['bias', 'flat', 'dark']
config.register.visit = ['calibDate']
