
from lsst.obs.base import MakeRawVisitInfoViaObsInfo
#from astro_metadata_translator import HuntsmanCamTranslator

#__all__ = ["MakeHuntsmanRawVisitInfo"]


class MakeHuntsmanRawVisitInfo(MakeRawVisitInfoViaObsInfo):
    """Make a VisitInfo from the FITS header of a Huntsman image
    """

    def __init__(self, *args, **kwargs):
        super().__init__()
