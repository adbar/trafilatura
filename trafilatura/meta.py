"""
Meta-functions to be applied module-wide.
"""

import gc

from courlan.meta import clear_caches as reset_caches_courlan
from htmldate.meta import reset_caches as reset_caches_htmldate
from justext.core import define_stoplist  # type: ignore

from .deduplication import LRU_TEST, Simhash, is_similar_domain
from .utils import line_processing, return_printables_and_spaces, trim


def reset_caches() -> None:
    """Reset all known LRU caches used to speed up processing.
       This may release some memory."""
    # justext
    define_stoplist.cache_clear()
    # handles htmldate and charset_normalizer
    reset_caches_htmldate()
    # courlan
    reset_caches_courlan()
    # own
    is_similar_domain.cache_clear()
    line_processing.cache_clear()
    return_printables_and_spaces.cache_clear()
    trim.cache_clear()
    LRU_TEST.clear()
    Simhash._vector_to_add.cache_clear()
    # garbage collection
    gc.collect()
