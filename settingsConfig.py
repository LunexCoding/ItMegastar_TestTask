from decouple import config


class _SettingsConfig:
    def __init__(self):
        self.__settingsConfig = self.__loadSettings()

    def __loadSettings(self):
        __settings = {}
        __settings["DATABASE"] = dict(
            host=config("DB_HOST"),
            port=config("DB_PORT", cast=int),
            user=config("DB_USER"),
            password=config("DB_PASSWORD"),
            database=config("DB_NAME")
        )
        return __settings

    @property
    def DatabaseSettings(self):
        return self.__settingsConfig["DATABASE"]


settingsConfig = _SettingsConfig()
