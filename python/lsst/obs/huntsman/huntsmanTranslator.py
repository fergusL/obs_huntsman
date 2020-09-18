"""
Metadata translator for Huntsman FITS headers.

See examples: https://github.com/lsst/astro_metadata_translator.
"""
from astropy import units as u

from astro_metadata_translator.translator import cache_translation
from astro_metadata_translator.translators.fits import FitsTranslator
from astro_metadata_translator.translators.helpers import tracking_from_degree_headers


class HuntsmanTranslator(FitsTranslator):

    name = "Huntsman"
    supported_instrument = "Huntsman"
    _const_map = {"boresight_rotation_coord": "sky"}

    _trivial_map = {"boresight_airmass": "AIRMASS",
                    "boresight_rotation_angle": "HA-MNT"}

    @cache_translation
    def to_tracking_radec(self):
        # Docstring will be inherited. Property defined in properties.py
        radecsys = None
        radecpairs = (("RA-MNT", "DEC-MNT"),)
        return tracking_from_degree_headers(self, radecsys, radecpairs, unit=(u.hourangle, u.deg))
