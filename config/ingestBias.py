from lsst.obs.huntsman.ingest import HuntsmanCalibsParseTask

config.parse.retarget(HuntsmanCalibsParseTask)

config.parse.translators = {'ccd': 'translate_ccd',
                            'calibDate': 'translate_calibDate'}

config.register.columns = {'ccd': 'int',
                           'calibDate': 'text',
                           'validStart': 'text',
                           'validEnd': 'text',
                           }

config.register.tables = ['bias']
config.register.unique = ['ccd', 'calibDate']
config.register.detector = ['ccd']
config.register.visit = ['calibDate']
