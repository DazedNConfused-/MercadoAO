import logging
from typing import Union

# Add TRACE-level capabilities to custom logger
# https://stackoverflow.com/a/13638084

TRACE_LEVELV_NUM = 9
logging.addLevelName(TRACE_LEVELV_NUM, "TRACE")


def trace(self, message, *args, **kws):
    if self.isEnabledFor(TRACE_LEVELV_NUM):
        # Yes, logger takes its '*args' as 'args'.
        self._log(TRACE_LEVELV_NUM, message, args, **kws)


# define Logger(Factory) here:


class Logger:
    @staticmethod
    def get_logger(name: str = None, level: Union[int, str] = logging.DEBUG) -> logging.Logger:
        # create logger
        logger = logging.getLogger(name)
        logger.setLevel(level)

        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(level)

        # create formatter
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)

        # add optional TRACE level to logger
        logging.Logger.trace = trace  # type: ignore

        # return result
        return logger
