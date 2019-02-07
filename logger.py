import logging
import sys

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def debug(msg):
    logger.debug(msg)

def error(msg):
    logger.error(msg)

def info(msg):
    logger.info(msg)

def warn(msg):
    logger.warn(msg)

def logger_to_stdout():
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

def set_verbose():
    logger.setLevel(logging.DEBUG)

def set_silent():
    logger.setLevel(logging.CRITICAL)