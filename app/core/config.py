import keyring

from logger import log
from app.core.settings import SETTINGS_JSON_PATH
from app.core.utils import Utils

from keyring.backends import Windows
keyring.set_keyring(Windows.WinVaultKeyring())


class Config:

    @staticmethod
    def get_schedule_url() -> str:
        try:
            return Utils.read_from_json(SETTINGS_JSON_PATH)["profile"]["personal_schedule"]
        except KeyError:
            log.error('key not found while getting schedule url')
        except:
            log.exception('unknown error while trying to get schedule URL')
        return ""


    @staticmethod
    def get_autostart() -> bool | None:
        try:
            return Utils.read_from_json(SETTINGS_JSON_PATH)["profile"]["autorun"]
        except KeyError:
            log.error('key not found when getting autostart value')
        except:
            log.exception('unknown error while trying to get autostart value')

    @staticmethod
    def get_password(login: str):
        try:
            return keyring.get_password("EduGhost", login)
        except:
            log.exception('when trying to get a password from Windows')

    @staticmethod
    def get_login() -> str:
        data = Utils.read_from_json(SETTINGS_JSON_PATH)
        if not data:
            log.error('empty data. PNS login data is empty')
            return ""
        return data["profile"]["login"]

    @staticmethod
    def set_password(username: str, password: str) -> None:
        keyring.set_password("EduGhost", username=username, password=password)
        log.info('password and login were saved in Windows')

    @staticmethod
    def is_auto_off():
        try:
            return Utils.read_from_json(SETTINGS_JSON_PATH)["profile"]["auto_off"]
        except:
            log.exception('unknown error trying to get windows automatic shutdown value')

    @staticmethod
    def clear_data():
        data = {
            "profile":
                {
                    "personal_schedule": "",
                    "autorun": False,
                    "shutdown": False,
                    "acceptTermsOfUse": False,
                    "login": "",
                    "id": 0,
                    "first_launch": ""
                }
        }
        Utils.write_to_json(SETTINGS_JSON_PATH, data)

    @staticmethod
    def check_user():
        if not keyring.get_password("EduGhost", Config.get_login()):
            Config.clear_data()