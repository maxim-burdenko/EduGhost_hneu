from bs4 import BeautifulSoup
from datetime import datetime
import requests
import re
from transliterate import translit

from back import settings as s
from back.utils import load_json, send_message_to_user



class ScheduleScraper:

    def __init__(self, web_driver, url:str='https://'):
        self.url = url
        self.driver = web_driver
        self.soup = self._get_soup()
        self.day_index = self._find_today_index()

    def _get_soup(self):
        try:
            response = requests.get(self.url)
            return BeautifulSoup(response.text, "lxml")
        except Exception as e:
            #send_message_to_user('Не вдалося відкрити сторінку з розкладом')
            print(f'[Error]: не удалось открыть расписание\n\n{e}\n\n')
            print('[Info]: не имея расписание, останавливаем приложения...')
            self.driver.quit()
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
            print('[Info]: возможно некорректная ссылка расписания')
            print('[Info]: таблица не была найдена')
            send_message_to_user('Не вдалося отримати розклад, перевірте власне посилання розкладу')
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
            except Exception as e:
                print(f'[Error]: Ошибка при извлечении данных\n\n{e}\n\n')

        return lesson_data

    def generate_schedule(self):
        if self.day_index is None:
            print("[Error]: не найден индекс сегодняшнего дня")
            print("[Error]: получить расписание не удалось")
            send_message_to_user('Не вдалося знайти сьогоднішній день')
            self.driver.quit()
            return

        schedule = []
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
                # print('[Error]: не найдено время')
                continue

            times = pair_timing_div.get_text("\n", strip=True).split("\n")
            start_time = times[0].split(' - ')[0]
            end_time = times[-1].split(' - ')[1]

            subject_td = td.find('td', id='subject')
            if subject_td:
                subject = re.sub(r'[\s\u200b]+', ' ', subject_td.get_text(strip=True)).strip()
                type_td = td.find('td', id='lessonType')
                subject_type = type_td.get_text(strip=True) if type_td else ""
                schedule.append({
                    "subject": subject,
                    "type": subject_type,
                    "start": start_time,
                    "end": end_time
                })
            else:
                for item in self._extract_lesson_info(td):
                    schedule.append({
                        "subject": item['name'],
                        "type": item['type'],
                        "start": start_time,
                        "end": end_time
                    })

        return schedule

    @staticmethod
    def generate_custom_schedule():
        today = datetime.today().strftime('%A')
        data = load_json(s.CUSTOM_SCHEDULE_JSON_PATH)
        schedule = []
        index = 1

        if not data:
            print('[Error]: пуст файл с кастомным расписанием ')
            return schedule

        return schedule

    @staticmethod
    def check_custom():
        data = load_json(s.SETTINGS_JSON_PATH)

        try:
            if data["profile"]["customSchedule"]:
                return True
            else:
                return False
        except Exception as e:
            print(f'[Error]: при получении настроек на customSchedule\n{e}\n\n')
            return False

# from back.services.browser_services import BrowserServices
# bs = BrowserServices()
# web_driver = bs.get_driver()
# # # Использование
# urls = "http://www.rozklad.hneu.edu.ua/schedule/schedule?group=37902&&student=446115"
# scraper = ScheduleScraper(urls, web_driver)
# schedule = scraper.generate_schedule()
# print(schedule)
