import asyncio
import os

from back.services.attendance_manager import AttendanceManager
from back.services.browser_services import BrowserServices
from back.services.pns_services import PnsServices
from back.services.zoom_services import ZoomServices
from back.services.schedule_scraper import ScheduleScraper
from back.settings import LINKS_JSON_PATH, prevent_sleep, allow_sleep, firefox_binary
from back.utils import (get_url_schedule, load_json, get_login, get_password, send_message_to_user,
                        change_status_to_user, check_shutdown)

async def run():
    web_driver = None
    try:
        if not firefox_binary:
            print('[Error]: не найден браузер Firefox. Программа продолжать работу не будет')
            send_message_to_user('Не знайдено браузера Firefox на Вашому ПК')
            change_status_to_user('збій', 'red')
            return

        prevent_sleep()
        bs = BrowserServices()
        web_driver = bs.get_driver("firefox")
        login = get_login()
        password = get_password()

        links = load_json(LINKS_JSON_PATH)
        pns = PnsServices(web_driver, bs, login, password)
        zoom = ZoomServices(web_driver)

        send_message_to_user('Скрипт було успішно запущено')
        change_status_to_user('активний', '#66ff00')
        schedule_url = get_url_schedule()
        schedule = ScheduleScraper(web_driver, schedule_url)
        am = AttendanceManager(pns, zoom, links, schedule_service=schedule)

        async with asyncio.TaskGroup() as tg:
            tg.create_task(am.process_zoom())
            tg.create_task(am.process_attendance())
    except Exception as e:
        send_message_to_user('Відбулася невідома помилка скрипта')
        change_status_to_user('збій', 'red')
        print(f'[Error]: при запуске скрипта\n{e}\n\n')
    finally:
        print('[Info]: завершаем работу скрипта...')

        allow_sleep()
        if web_driver: web_driver.quit()
        if check_shutdown():
            print('[INFO]: отключаем ПК через 5 минут')
            os.system('shutdown /s /f /t 300')
        else:
            print('[INFO]: ПК не отключаем. Остается работать')

        print('[INFO]: работа скрипта завершена...')
        send_message_to_user('Скрипт було завершено без помилок')
        change_status_to_user('не активний', '#ff2d15')
        return

def start():
    try:
        print('[Info]: запуск скрипта...')
        asyncio.run(run())
    except Exception as e:
        print(f'[Error]: при выполнении скрипта\n\n{e}\n')
    finally:
        print('[Info]: скрипт завершил работу')