import re

from app.core.utils import Utils
from app.core.settings import LINKS_JSON_PATH
from logger import log

class LinkViewModel:
    def __init__(self):
        self.utils = Utils()

        self.zoom_regex = r"^https://us02web\.zoom\.us/j/\d{11}\?pwd=[A-Za-z0-9]+&uname=[^#]+#success$"
        self.pns_regex = r"^https://pns\.hneu\.edu\.ua/mod/attendance/view\.php\?id=\d+$"

    def add_lesson(self, name:str, lecture_zoom:str, practice_zoom:str, laboratory_zoom:str,
                   lecture_attendance:str, practice_attendance:str, laboratory_attendance:str) -> list[tuple[str, str]]:

        info = []


        if not name.strip():
            log.warning('була пуста назва пари, нічого не зберігаємо')
            info.append(("name", "назва пари не може бути порожньою"))
            return info

        lesson = {
            name:{
                "lecture": {
                    "zoom": "",
                    "attendance": ""
                },
                "practice": {
                    "zoom": "",
                    "attendance": ""
                },
                "laboratory": {
                    "zoom": "",
                    "attendance": ""
                }
            }
        }

        if lecture_zoom.strip() and re.match(self.zoom_regex, lecture_zoom):
            log.debug('додано локально Zoom лекцію')
            lesson[name]["lecture"]["zoom"] = lecture_zoom
            info.append(("lecture_zoom", ""))
        elif not lecture_zoom.strip():
            info.append(("lecture_zoom", ""))
            pass
        else:
            info.append(("lecture_zoom", "невірний формат введення. Має бути так\n"
            "https://us02web.zoom.us/j/11_чисел?pwd=тільки_англ_літери_та_цифри&uname=ваше_ім'я#success"))

        if practice_zoom.strip() and re.match(self.zoom_regex, practice_zoom):
            log.debug('додано локально Zoom практична')
            lesson[name]["practice"]["zoom"] = practice_zoom
            info.append(("practice_zoom", ""))
        elif not practice_zoom.strip():
            info.append(("practice_zoom", ""))
            pass
        else:
            info.append(("practice_zoom", "невірний формат введення. Має бути так\n"
            "https://us02web.zoom.us/j/11_чисел?pwd=тільки_англ_літери_та_цифри&uname=ваше_ім'я#success"))

        if laboratory_zoom.strip() and re.match(self.zoom_regex, laboratory_zoom):
            log.debug('додано локально Zoom лабораторна')
            lesson[name]["laboratory"]["zoom"] = laboratory_zoom
            info.append(("laboratory_zoom", ""))
        elif not laboratory_zoom.strip():
            info.append(("laboratory_zoom", ""))
            pass
        else:
            info.append(("laboratory_zoom", "невірний формат введення. Має бути так\n"
            "https://us02web.zoom.us/j/11_чисел?pwd=тільки_англ_літери_та_цифри&uname=ваше_ім'я#success"))

        if lecture_attendance.strip() and re.match(self.pns_regex, lecture_attendance):
            log.debug('додано локально відвідування лекція')
            lesson[name]["lecture"]["attendance"] = lecture_attendance
            info.append(("lecture_attendance", ""))
        elif not lecture_attendance.strip():
            info.append(("lecture_attendance", ""))
            pass
        else:
            info.append(("lecture_attendance", "невірний формат введення. Має бути так\n"
        "https://pns.hneu.edu.ua/mod/attendance/view.php?id=числа"))

        if practice_attendance.strip() and re.match(self.pns_regex, practice_attendance):
            log.debug('додано локально відвідування практична')
            lesson[name]["practice"]["attendance"] = practice_attendance
            info.append(("practice_attendance", ""))
        elif not practice_attendance.strip():
            info.append(("practice_attendance", ""))
            pass
        else:
            info.append(("practice_attendance", "невірний формат введення. Має бути так\n"
                    "https://pns.hneu.edu.ua/mod/attendance/view.php?id=числа"))

        if laboratory_attendance.strip() and re.match(self.pns_regex, laboratory_attendance):
            log.debug('додано локально відвідування лабораторна')
            lesson[name]["laboratory"]["attendance"] = laboratory_attendance
            info.append(("laboratory_attendance", ""))
        elif not laboratory_attendance.strip():
            info.append(("laboratory_attendance", ""))
            pass
        else:
            info.append(("laboratory_attendance", "невірний формат введення. Має бути так\n"
                "https://pns.hneu.edu.ua/mod/attendance/view.php?id=числа"))

        self.utils.update_to_json(LINKS_JSON_PATH, lesson)
        return info


    def get_lesson_by_key(self, key:str) -> dict:
        data = self.utils.read_from_json(LINKS_JSON_PATH)

        if not data:
            log.warning('посилання пусті, нічого змінювати')
            return {}

        if not key in data:
            log.error('%r не знайдено в списку')
            return {}

        return {key: data[key]}
