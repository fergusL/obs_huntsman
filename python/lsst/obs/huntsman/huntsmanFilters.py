"""
- lambdaMin and lambdaMax are chosen to be where the filter rises above 1%
- physical_filter specifies names of individual pieces of glass (1 per filter per lens)
- abstract_filter is the generic name of the filter
- See: https://github.com/lsst/obs_base/blob/769a877cad0ce0996a796bb2e0cfcd1832815f13/python/lsst/obs/base/filters.py
"""
from lsst.obs.base import FilterDefinition, FilterDefinitionCollection

# Note that these aren't the proper measurements, just guesses for now.

HUNTSMAN_FILTER_DEFINITIONS = FilterDefinitionCollection(
    FilterDefinition(physical_filter="g2_8",
                     abstract_filter="g2",
                     lambdaEff=550, lambdaMin=500, lambdaMax=600),
)
