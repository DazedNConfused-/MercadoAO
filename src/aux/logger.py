import logging
from typing import Union

TRACE_LEVELV_NUM = 9
logging.addLevelName(TRACE_LEVELV_NUM, "TRACE")


class Logger(logging.Logger):
    def __init__(self, name: str, level: Union[int, str] = logging.DEBUG) -> None:
        super().__init__(name, level)

        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(level)

        # create formatter
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        self.addHandler(ch)

    def trace(self, message, *args, **kws) -> None:
        """
        Log a message with severity 'TRACE' on the root logger. If the logger has
        no handlers, call basicConfig() to add a console handler with a pre-defined
        format.
        """

        # Add TRACE-level capabilities to custom logger
        # https://stackoverflow.com/a/13638084

        if self.isEnabledFor(TRACE_LEVELV_NUM):
            # yes, logger takes its '*args' as 'args'.
            self._log(TRACE_LEVELV_NUM, message, args, **kws)
