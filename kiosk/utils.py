import logging as log
from logging.handlers import RotatingFileHandler
import os
import time

# TODO Just started with converting logging to use RotatingFileHandler

log_level = log.DEBUG
log.basicConfig(level=log_level, format='{%(asctime)s} [%(levelname)-8s]: %(message)s',
                    filename=f"{time.strftime('%Y-%m-%d %H%M%S')}.log", filemode='w')

def log_debug():
    log.basicConfig(level=log.DEBUG, format='{%(asctime)s} [%(levelname)-8s]: %(message)s',
                    filename=f"{time.strftime('%Y-%m-%d %H%M%S')}.log", filemode='w')


logger = log.getLogger("wrap_func_logger")

def log_func(pre, post):
    """ Wrapper """
    def decorate(func):
        """ Decorator """
        def call(*args, **kwargs):
            """ Actual wrapping """
            pre(func, *args)
            result = func(*args, **kwargs)
            post(func)
            return result
        return call
    return decorate


def entering(func, *args):
    """ Pre function logging """
    logger.debug("Entered %s", func.__name__)
    logger.info(func.__doc__)
    logger.info("Function at line %d in %s" %
        (func.__code__.co_firstlineno, func.__code__.co_filename))
    try:
        if len(args) == 0:
            logger.warn("No arguments.")
        else:
             logger.warn("The argument %s is %s" % (func.__code__.co_varnames[0], *args))
    except IndexError:
        logger.warn("No arguments")
    except TypeError:
        logger.warn("No arguments")


def exiting(func):
    """ Post function logging """
    logger.debug("Exited  %s", func.__name__)

