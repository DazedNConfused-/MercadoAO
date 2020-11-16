from __future__ import annotations

import gettext
from collections import Callable
from typing import Optional

from src.aux.logger import TRACE_LEVELV_NUM, Logger
from src.aux.singleton import Singleton

LOCALE_EN: str = "en"
LOCALE_ES_AR: str = "es_AR"


class I18n(metaclass=Singleton):
    """
    Class in charge of providing internationalization support. Based on GNU's gettext.

    In order to initialize the I18n module, call this once at the topmost-layer of the application:
        i18n = I18n().with_lang(LOCALE).init()

    In order to make use of internationalized texts, import this at the top of each class where strings should be
    parsed:
        _: Callable[[str], str] = lambda s: I18n().gettext(s)

    And to use it:
        _(<text_to_translate>)

    https://phrase.com/blog/posts/translate-python-gnu-gettext/
    https://stackoverflow.com/questions/18822396/flask-babel-updating-of-existing-messages-pot-file
    """

    def __init__(self) -> None:
        super().__init__()

        self._logger = Logger(self.__class__.__name__, TRACE_LEVELV_NUM)
        self._logger.info("Initializing internationalization (l18n) module...")

        self._language: str = LOCALE_EN
        self._gettext: Optional[Callable[[str], str]] = None

    def with_lang(self, language: str) -> I18n:
        self._logger.info("Loading language {}...".format(language))
        self._language = language

        # since the i18n module is a singleton shared across all modules, language overload gets disabled upon
        # initialization
        self.with_lang = lambda lang: self._disable_i18n_re_init()  # type: ignore

        return self

    def init(self) -> I18n:
        el = gettext.translation(domain="messages", localedir="locales", languages=[self._language])
        el.install()
        self._gettext = el.gettext  # update gettext's call with installed language

        self._logger.info(
            "Internationalization module initialized successfully. Loaded language: {}.".format(self._language)
        )
        self._logger.debug(
            "*Note*: locale hot-swapping is not supported. "
            "If another language is desired, change configuration and restart application."
        )

        # since the i18n module is a singleton shared across all modules, we shall disable future 're'-inits of the
        # module
        self.init = self._disable_i18n_re_init  # type: ignore

        return self

    def _disable_i18n_re_init(self) -> I18n:
        self._logger.debug(
            "Internationalization module already initialized with language: {}. "
            "Re-initizalization is not supported.".format(self._language)
        )
        return self

    @property
    def gettext(self) -> Callable[[str], str]:
        if self._gettext is None:
            self._logger.debug(
                "Internationalization module was not initialized. A default implementation of 'gettext' will be "
                "returned. Translations will most probably not work."
            )
            self._logger.trace(
                "In order to initialize the i18n module properly, call: \n\n"
                ">>> I18n().with_lang(LOCALE_ES_AR).init().\n\n"
                "Afterwards, once initialized, gettext's function can be declared as: \n\n"
                ">>> _: Callable[[str], str] = lambda s: I18n().gettext(s)\n"
            )
            return gettext.gettext
        return self._gettext
