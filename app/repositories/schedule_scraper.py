from bs4 import BeautifulSoup
from datetime import datetime
import requests
import re
from transliterate import translit

from app.core import settings as s
from app.core.config import Config
from app.core.settings import MAPPED_TYPE_LESSON
from app.models.schedule import Schedule
from app.models.lesson import Lesson

from logger import log

class ScheduleScraper:

    def __init__(self, url:str):
        if not url:
            self.url = Config.get_schedule_url()
        self.url = url
        self.soup = self._get_soup()
        self.day_index = self._find_today_index()

    def _get_soup(self):
        try:
            response = requests.get(self.url)
            return BeautifulSoup(response.text, "lxml")
        except:
            log.exception('невідома помилка при отриманні розкладу')
            log.debug('зупиняю скрипт...')
            return


    @staticmethod
    def _get_current_date():
        now = datetime.now()
        month_en = now.strftime("%B")
        day = now.strftime("%d")
        year = now.strftime("%Y")
        return f"{day} {s.MONTHS_UK[month_en]} {year}".lower().lstrip("0")

    def _find_today_index(self):
        schedule_table = self.soup.find("table")
        if not schedule_table:
            log.warning('не вдалося отримати розклад, скоріше помилка у посиланні')
            return None

        header_cells = schedule_table.find_all("th")
        current_date = self._get_current_date()

        current_date_trans = translit(current_date, 'uk', reversed=True)

        for i, th in enumerate(header_cells):
            if th.get("title") == "Сьогоднішній день":

                date_text = th.find("td", id="date").text.strip().lower().lstrip("0")
                date_text_trans = translit(date_text, 'uk', reversed=True)

                if current_date_trans == date_text_trans:
                    return i
        return None

    @staticmethod
    def _extract_lesson_info(td_element):
        lesson_data = []
        tables = td_element.find_all("table")

        for table in tables:
            try:
                subject_td = table.find("td", {"id": "subject-small"})
                lesson_type_td = table.find("td", {"id": "lessonType-small"})

                if subject_td and lesson_type_td:
                    subject_text = re.sub(r'[\s\u200b]+', ' ', subject_td.get_text(strip=True)).strip()
                    lesson_type_text = re.sub(r'[\s\u200b]+', ' ', lesson_type_td.get_text(strip=True)).strip()

                    lesson_data.append({
                        'name': subject_text,
                        'type': lesson_type_text
                    })
            except:
                log.exception('невідома помилка при отримані даних')

        return lesson_data

    def generate_schedule(self) -> Schedule | None:
        if self.day_index is None:
            log.error('не знайдено index сьогоднішнього дня')
            log.debug('можливо ліг сама сторінку розкладу')
            return None

        lessons = []
        rows = [tr for table in self.soup.find_all('table') for tr in table.find_all('tr', recursive=False)]

        for row in rows:
            tds = row.find_all('td', recursive=False)

            if self.day_index >= len(tds):
                continue

            td = tds[self.day_index]
            if not td or (td.find('div', recursive=False) and td.find('div').get('id') == 'empty'):
                continue

            pair_timing_div = row.find('div', id='pair-timing')
            if not pair_timing_div:
                continue

            times = pair_timing_div.get_text("\n", strip=True).split("\n")
            try:
                start_time = times[0].split(' - ')[0]
                end_time = times[-1].split(' - ')[1]
            except IndexError:
                continue

            subject_td = td.find('td', id='subject')
            if subject_td:
                subject = re.sub(r'[\s\u200b]+', ' ', subject_td.get_text(strip=True)).strip()
                type_td = td.find('td', id='lessonType')
                subject_type = type_td.get_text(strip=True) if type_td else ""

                if subject_type in MAPPED_TYPE_LESSON:
                    subject_type = MAPPED_TYPE_LESSON[subject_type]

                lessons.append(Lesson(name=subject, type_=subject_type, start=start_time, end=end_time))
            else:
                for item in self._extract_lesson_info(td):
                    lessons.append(Lesson(name=item['name'], type_=item['type'], start=start_time, end=end_time))

        return Schedule(lessons=lessons)
