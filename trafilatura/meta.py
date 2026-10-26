"""
Meta-functions to be applied module-wide.
"""

import gc

from courlan.meta import clear_caches as reset_caches_courlan
from htmldate.meta import reset_caches as reset_caches_htmldate
from justext.core import define_stoplist

from .deduplication import LRU_TEST, _vector_to_add, is_similar_domain
from .external import get_stoplist, jt_stoplist_init
from .readability_lxml import _attribute_weight
from .utils import line_processing, return_printables_and_spaces, trim


def reset_caches() -> None:
    """Reset all known LRU caches used to speed up processing.
    This may release some memory."""
    # justext
    define_stoplist.cache_clear()
    get_stoplist.cache_clear()
    jt_stoplist_init.cache_clear()
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
    _vector_to_add.cache_clear()
    _attribute_weight.cache_clear()
    # garbage collection
    gc.collect()
