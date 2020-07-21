'''
Override the default calibrate config parameters by putting them in here.
e.g.:
config.doAstrometry = False

Useful info for photocal:
https://community.lsst.org/t/reference-catalogs-camfluxes-and-colorterms/3578
https://community.lsst.org/t/pan-starrs-reference-catalog-in-lsst-format/1572
http://doxygen.lsst.codes/stack/doxygen/x_11_0/load_reference_objects_8py_source.html

For setting up filters:
https://community.lsst.org/t/failure-finding-flux-fields-in-processeimages-py/2486/2
'''
from lsst.meas.algorithms import LoadIndexedReferenceObjectsTask
from lsst.pipe.tasks.colorterms import ColortermDict, Colorterm

REFCAT = "skymapper_dr3"

config.astromRefObjLoader.retarget(LoadIndexedReferenceObjectsTask)
config.astromRefObjLoader.ref_dataset_name = REFCAT
config.photoRefObjLoader.retarget(LoadIndexedReferenceObjectsTask)
config.photoRefObjLoader.ref_dataset_name = REFCAT
config.photoCal.photoCatName = REFCAT
config.connections.astromRefCat = REFCAT
config.connections.photoRefCat = REFCAT

config.doPhotoCal = True
config.doAstrometry = True

# These colorterms are for HSC, included as an example
"""
colorterms = config.calibrate.photoCal.colorterms
colorterms.data["ps1*"] = ColortermDict(data={
    'g': Colorterm(primary="g", secondary="r", c0=0.00730066, c1=0.06508481, c2=-0.01510570),
    'r': Colorterm(primary="r", secondary="i", c0=0.00279757, c1=0.02093734, c2=-0.01877566),
    'r2': Colorterm(primary="r", secondary="i", c0=0.00117690, c1=0.00003996, c2=-0.01667794),
    'i': Colorterm(primary="i", secondary="z", c0=0.00166891, c1=-0.13944659, c2=-0.03034094),
    'i2': Colorterm(primary="i", secondary="z", c0=0.00180361, c1=-0.18483562, c2=-0.02675511),
    'z': Colorterm(primary="z", secondary="y", c0=-0.00907517, c1=-0.28840221, c2=-0.00316369),
    'y': Colorterm(primary="y", secondary="z", c0=-0.00156858, c1=0.14747401, c2=0.02880125),
})
"""
# Specify mappings between Huntsman and Skymapper filters
for refObjLoader in (config.astromRefObjLoader,
                     config.photoRefObjLoader,
                     ):
    refObjLoader.filterMap['g2'] = 'g_psf'
    # refObjLoader.filterMap['i2'] = 'i'
