from app.core.config import Config
from app.core.utils import Utils
from app.schemes.user_shcema import UserSchema
from logger import log
import re

class ProfileViewModel:
    def __init__(self):
        self.utils = Utils()
        self.config = Config
        self.user = UserSchema.load()

        self.regex_url = r"^http://www\.rozklad\.hneu\.edu\.ua/schedule/schedule\?group=\d{5}&student=\d{6}$"

    def add_data_profile(self, url:str, log_:str, pass_:str):
        info = []

        if not url.strip() and not log_.strip() and not pass_.strip():
            self.user.login = ""
            self.user.personal_schedule = ""
            self.user.save()
            log.debug('було очищено логін, пароль та посилання')


        if url.strip() and re.match(self.regex_url, url):
            self.user.personal_schedule = url
            self.user.save()
            log.debug('посилання було збережено')
            info.append(("url", ""))
        elif not url:
            pass
        else:
            log.debug('посилання було введено проте воно не правильне')
            info.append(("url", "посилання не вірного формату"))


        if not log_.strip() and not pass_.strip():
            return info

        if log_ and pass_ and log_.strip() and pass_.strip():
            self.user.login = log_
            self.config.set_password(username=log_, password=pass_)
            self.user.save()
            log.debug('логін та пароль були збережені')
        else:
            log.debug('чогось не було, або логіну або пароля')
            info.append(("log_pass", "неможливо внести тільки логін або тільки пароль"))

        return info

    def set_autorun(self, value:bool):
        self.user.autorun = value
        self.user.save()
        log.debug('значення автозавантаження встановлено на %s', value)

    def get_autorun(self):
        return self.user.autorun

    def set_auto_off(self, value:bool):
        self.user.auto_off = value
        self.user.save()
        log.debug('значення автоматичного виключення Windows встановлено на %s', value)

    def get_auto_off(self):
        return self.user.auto_off

    def get_url(self):
        if self.user.personal_schedule:
            return self.user.personal_schedule
        else:
            return 'ще не було додано'

    def get_login(self):
        if self.user.login:
            return self.user.login
        else:
            return 'ще не було додано'

    def get_password(self):
        if self.user.login:
            return "було додано"
        else:
            return 'ще не було додано'