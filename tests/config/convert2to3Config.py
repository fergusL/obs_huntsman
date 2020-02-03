# Config overrides for `test_convert2to3.py`
# These are designed to replace the `config/convertRepo.py` settings that are
# not relevant for testdata_subaru.

config.skyMaps = {}
config.rootSkyMapName = None
config.refCats = []
del config.collections["ps1_pv3_3pi_20170110"]
