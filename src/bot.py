from discord.ext import commands

from src.aux.logger import Logger


class MercadoAO(commands.Bot):
    """
    MercadoAO's Discord Client. Soft wrapper around discord.py's bot library.
    """

    def __init__(self, **options):
        super().__init__(**options)

        self._logger = Logger.get_logger(self.__class__.__name__)

        self._logger.info("=== Initializing MercadoAO Discord Bot ===")
        # bot will be truly ready when the on_ready() function gets called

    async def on_ready(self):
        self._logger.debug("Logged on as {0}!".format(self.user))
        self._logger.info("=== MercadoAO initialized ===")
