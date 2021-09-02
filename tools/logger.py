# _*_ coding: utf-8 _*_
# _*_ author_by zn _*_

from functools import wraps
import logging


def logger(level, name=None, message=None):

    def decorate(func):

        logname = name if name else func.__module__
        logmsg = message if message else func.__name__

        # create logger
        logger = logging.getLogger(logname)
        logger.setLevel(logging.DEBUG)

        # create file handler
        log_path = 'expansion_api.log'
        fh = logging.FileHandler(log_path)

        # create formatter
        fmt = "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s"
        dateFmt = "%a %d %b %Y %H:%M:%S"
        formatter = logging.Formatter(fmt, dateFmt)

        @wraps(func)
        def wrapper(*args, **kwargs):

            # add handler and formatter to logger
            fh.setFormatter(formatter)
            logger.addHandler(fh)

            logger.log(level, logmsg)

            try:
                return func(*args, **kwargs)

            except Exception as e:
                logger.error(e)

        return wrapper

    return decorate


