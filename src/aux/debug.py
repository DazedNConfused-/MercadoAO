from src.aux.logger import Logger


class Debug:
    """
    This class includes environmental settings and code that should run on non-production environments for debugging
    purposes.
    """

    def __init__(self) -> None:
        self._logger = Logger(self.__class__.__name__)
        self._logger.debug("Debug mode is active. Additional development features are enabled.")

        import pretty_errors

        pretty_errors.configure(
            separator_character="*",
            filename_display=pretty_errors.FILENAME_EXTENDED,
            line_number_first=True,
            display_link=True,
            lines_before=5,
            lines_after=2,
            line_color=pretty_errors.RED + "> " + pretty_errors.default_config.line_color,
            code_color="  " + pretty_errors.default_config.line_color,
            truncate_code=True,
            display_locals=False,
        )
