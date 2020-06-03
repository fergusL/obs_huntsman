from lsst.obs.huntsman.ingest import HuntsmanCalibsParseTask

config.parse.retarget(HuntsmanCalibsParseTask)

config.parse.translators = {'filter': 'translate_filter',
                            'ccd': 'translate_ccd',
                            'calibDate': 'translate_calibDate',
                            'expTime': 'translate_expTime'}

config.register.columns = {'filter': 'text',
                           'ccd': 'int',
                           'expTime': 'double',
                           'calibDate': 'text',
                           'validStart': 'text',
                           'validEnd': 'text',
                           }

config.register.tables = ['bias', 'dark']
config.register.visit = ['calibDate']
