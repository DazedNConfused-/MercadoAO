import configparser
import os.path
from typing import Any, Dict, Mapping, Optional

CONFIGURATION_FILE = "config.ini"

DEFAULT_ROOT = "MERCADOAO"

DISCORD_TOKEN_KEY = "discord_token"
ANNOUNCEMENT_CHANNEL_ID_KEY = "announcement_channel_id"


class Configuration:
    """Application's global configuration. If a configurable parameter isn't in here, then it doesn't exist."""

    def __init__(self):
        self._config = configparser.ConfigParser()  # initialize config manager

        self._config.read_dict(self.build_defaults())  # load defaults

        if not os.path.exists(CONFIGURATION_FILE):
            self.save_config()  # if .ini file is not present (first run or was erased), save loaded defaults
        else:
            self._config.read(
                CONFIGURATION_FILE
            )  # if .ini file exists, then it may have overloaded parameters. Load it

    def save_config(self):
        """Saves the current configuration as a .ini file in the filesystem."""
        with open(CONFIGURATION_FILE, "w") as configfile:
            self._config.write(configfile)

    def get_discord_token(self) -> str:
        """Returns MercadoAO's Discord token"""
        return self._config[DEFAULT_ROOT][DISCORD_TOKEN_KEY]

    def get_announcement_channel_id(self) -> Optional[int]:
        """Returns MercadoAO's announcement channel"""
        if self._config[DEFAULT_ROOT][ANNOUNCEMENT_CHANNEL_ID_KEY]:
            return int(self._config[DEFAULT_ROOT][ANNOUNCEMENT_CHANNEL_ID_KEY])
        else:
            return None

    @staticmethod
    def build_defaults() -> Mapping[str, Mapping[str, Any]]:
        """Builds the default configuration mapping."""
        config: Dict[str, Any] = dict()

        config[DEFAULT_ROOT] = {DISCORD_TOKEN_KEY: "", ANNOUNCEMENT_CHANNEL_ID_KEY: ""}

        return config
