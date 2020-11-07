import logging
from typing import Union


class Logger:
    @staticmethod
    def get_logger(
        name: str = None, level: Union[int, str] = logging.DEBUG
    ) -> logging.Logger:
        # create logger
        logger = logging.getLogger(name)
        logger.setLevel(level)

        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(level)

        # create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)

        # return result
        return logger
