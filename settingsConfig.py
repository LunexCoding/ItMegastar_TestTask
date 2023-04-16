import json
import typing
from decouple import config
from starlette.responses import Response


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


class PrettyJSONResponse(Response):
    media_type = "application/json"

    def render(self, content: typing.Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=4,
            separators=(", ", ": "),
        ).encode("utf-8")


settingsConfig = _SettingsConfig()
