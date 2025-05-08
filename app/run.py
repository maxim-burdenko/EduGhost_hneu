import asyncio
import os
import time
from asyncio import CancelledError

from pyexpat.errors import messages

from app.models.browser import Browser
from app.repositories.attendance_manager import MainManager

from app.repositories.pns_services import PnsRepository
from app.repositories.zoom_services import ZoomServices
from app.repositories.schedule_scraper import ScheduleScraper
from app.core.settings import LINKS_JSON_PATH, prevent_sleep, allow_sleep, firefox_binary
from app.core.utils import Utils
from app.core.config import Config
from app.schemes.user_shcema import UserSchema

from app.status_handler import StatusHandler


from logger import log

main_task = None
running = False
tasks = []

handler = StatusHandler()
message = False

async def run():

    global tasks, running, message

    handler.status ="в процесі"
    web_driver = None
    zoom = None

    user = UserSchema.load()
    log.info('try running the script...')
    try:
        if not firefox_binary:
            log.error('не знайдено браузер Firefox. Програма продовжувати роботу не буде')
            handler.status = "немає Firefox"
            message = True
            return

        if not user.login:
            log.debug('not fill login')
            handler.status = "немає логіну"
            message = True
            return

        password = Config.get_password(user.login)
        schedule_url = Config.get_schedule_url()
        links = Utils.read_from_json(LINKS_JSON_PATH)

        if not password:
            user.clear()
            return
        if not schedule_url:
            log.error('немає посилання для розкладу')
            handler.status = "немає розкладу"
            message = True
            return
        if not links:
            log.error('немає посилань')
            handler.status = "немає посилань"
            message = True
            return

        prevent_sleep()
        browser = Browser()

        try:
            schedule = ScheduleScraper(schedule_url).generate_schedule().lessons
        except AttributeError:
            log.error('не вдалося отримати розклад з сайту')
            log.debug(schedule_url)
            handler.status = "збій з розкладом"
            message = True
            return

        if not schedule:
            log.info('на сьогодні пар немає, відпочиваємо')
            handler.status = "пар немає"
            message = True
            return

        log.debug('load a driver...')
        web_driver = await browser.driver
        log.debug('driver loaded')


        zoom = ZoomServices(web_driver)
        pns = PnsRepository(username=user.login, password=password, web_driver=web_driver)
        am = MainManager(pns, zoom, links, schedule)

        handler.status = "активний"

        t1 = asyncio.create_task(am.zoom_meet_processing())
        t2 = asyncio.create_task(am.attendance_processing())
        tasks = [t1, t2]

        try:
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            handler.status = "відміна"
            log.warning('main thread was canceled')
            for task in tasks:
                task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
            raise

    except CancelledError:
        handler.status = "відміна"
        log.warning('was interrupted work script')
    except:
        handler.status = "збій"
        message = True
        log.exception('невідома помилка при запуску/виконанні скрипта')
    finally:

        log.info('завершуємо роботу скрипта')

        if web_driver: web_driver.quit()
        if user.auto_off:
            try:
                now = await Utils().get_kyiv_now(format_datetime=True)
                end = now.strftime('%H:%M')
                date = now.strftime('%d-%m-%Y')
                Utils().first_launch(date)
                Utils().activity_app(user.start, end, date, "run", user.auto_off, user.autorun)
            except:
                log.debug('error activity')

            log.info('відключення ПК відбудеться через 5 хвилин')
            os.system('shutdown /s /f /t 300')
        else:
            log.warning('ПК не буду виключено автоматично')
            allow_sleep()

        if not message:
            handler.status = "неактивний"

        log.info('робота скрипта завершена')
        running = False
        time.sleep(2)
        if zoom:
            await zoom.kill()
            time.sleep(8)
            await zoom.kill()

        return



async def start():
    global running, main_task
    if not running:
        running = True
        Utils.running = True
        main_task = asyncio.create_task(run())
    else:
        log.info('already launched')

async def stop():
    global main_task, running
    if running and main_task:
        log.warning('Stopping script...')
        main_task.cancel()
        try:
            await main_task
        except asyncio.CancelledError:
            pass
        log.info("The script has stopped completely.")
        Utils.running = False
        running = False