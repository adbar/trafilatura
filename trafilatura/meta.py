"""
Meta-functions to be applied module-wide.
"""

from courlan.urlutils import get_tldinfo
from htmldate.meta import reset_caches as reset_caches_htmldate
from justext.core import define_stoplist

from .filters import LRU_TEST
from .hashing import Simhash
from .utils import line_processing, return_printables_and_spaces, trim


def reset_caches() -> None:
    """Reset all known LRU caches used to speed-up processing.
    This may release some memory."""
    # justext
    define_stoplist.cache_clear()
    # handles htmldate and charset_normalizer
    reset_caches_htmldate()
    # courlan
    get_tldinfo.cache_clear()
    # own
    line_processing.cache_clear()
    return_printables_and_spaces.cache_clear()
    trim.cache_clear()
    LRU_TEST.clear()
    Simhash._vector_to_add.cache_clear()
