#!/usr/bin/python3
# -*- coding: utf-8 -*-


# logging.basicConfig(filename='example.log',level=logging.DEBUG)
# https://docs.python.org/3/howto/logging.html#logging-advanced-tutorial

#import logging

#try:  # Python 2.7+
#    from logging import NullHandler
#except ImportError:
#    class NullHandler(logging.Handler):
#        def emit(self, record):
#            pass
#logging.getLogger(__name__).addHandler(NullHandler())



## extract
#MIN_EXTRACTED_SIZE = 200
#MIN_DUPLCHECK_SIZE = 100
#CORPUS_VERSION = 2017.1
#LRU_SIZE = 10000000
# MIN_EXTRACTED_COMM_SIZE = 100

# filters
# LANG = 'de'

## logging
#def setup_logger(name, log_file, level=logging.INFO):
#    """Formatting loggers using unified settings"""
#    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#    file_log_handler = logging.FileHandler(log_file)
#    file_log_handler.setFormatter(formatter)
#    logger = logging.getLogger()
#    logger.addHandler(file_log_handler)
#    logger.setLevel(level)
#    return logger