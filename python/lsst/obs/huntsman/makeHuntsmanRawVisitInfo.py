
from lsst.obs.base import MakeRawVisitInfoViaObsInfo
#from astro_metadata_translator import HuntsmanCamTranslator

#__all__ = ["MakeHuntsmanRawVisitInfo"]


class MakeHuntsmanRawVisitInfo(MakeRawVisitInfoViaObsInfo):
    """Make a VisitInfo from the FITS header of a Subaru SuprimeCam image
    """

    # Force HSC Translator.  Not required but being explicit does no harm.
    #metadataTranslator = HuntsmanCamTranslator
