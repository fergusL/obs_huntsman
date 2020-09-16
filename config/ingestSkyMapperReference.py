"""
Documentation:
https://pipelines.lsst.io/modules/lsst.meas.algorithms/creating-a-reference-catalog.html
https://pipelines.lsst.io/modules/lsst.meas.algorithms/tasks/lsst.meas.algorithms.IngestIndexedReferenceTask.html#lsst-meas-algorithms-ingestindexedreferencetask-configs
"""
# The name of the output reference catalog dataset.
config.dataset_config.ref_dataset_name = "skymapper_dr3"

# Gen3 butler wants all of our refcats have the same indexing depth.
config.dataset_config.indexer['HTM'].depth = 7

# Ingest the data in parallel with this many processes.
config.n_processes = 8

# These define the names of the fields from the gaia_source data model:
# http://skymapper.anu.edu.au/table-browser/

config.id_name = "object_id"
config.ra_name = "raj2000"
config.dec_name = "dej2000"
config.ra_err_name = "e_raj2000"
config.dec_err_name = "e_dej2000"
config.coord_err_unit = "arcsec"

# All or none of these should be set
# config.epoch_name = "mean_epoch"
# config.epoch_format = "mjd"
# config.epoch_scale = ???

config.mag_column_list = ["u_psf", "g_psf", "r_psf", "i_psf", "z_psf"]
config.mag_err_column_map = {s: f"e_{s}" for s in config.mag_column_list}
