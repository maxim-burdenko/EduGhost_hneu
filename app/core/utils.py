import json
import os
import random
import aiohttp
import requests

from datetime import datetime, timedelta, UTC
from dotenv import load_dotenv

from logger import log
from app.core.settings import LINKS_JSON_PATH, SETTINGS_JSON_PATH, PATH_ENV, VERSION


class Utils:
    """ клас потрібен для усіх можливих додаткових операція, таких як отримання сторінки,
    читання/запис/оновленння файлу з перевіркою на помилки, та багато іншого для оботи застосунку """

    running = False
    changed_links = False

    def __init__(self):
        self.stop_script = False
        self._cached_time = None
        self._last_fetched = None
        load_dotenv(PATH_ENV)

    @staticmethod
    def read_from_json(filepath: str) -> dict:
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                data = file.read() # важається, щр файле не великі
                if not data or data.strip() == '{}':
                    log.error('file %s is empty', filepath)
                    return {}
                return json.loads(data)
        except FileNotFoundError:
            log.error('file by path %s was not found', filepath)
        except json.JSONDecodeError:
            log.exception('error decoding file %s', filepath)
        except ValueError:
            log.error('error load file %s', filepath)
        except:
            log.exception('unknown error reading file %s', filepath)

        return {}

    @staticmethod
    def write_to_json(filepath: str, data: dict, debug=False) -> bool:
        """Перезаписываем JSON-файл с новыми данными."""
        if not data:
            log.warning('empty data will be writing')

        if debug:
            log.debug(data)

        try:
            json_data = json.dumps(data, indent=2, ensure_ascii=False)
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(json_data)      # Expected type 'SupportsWrite[str]', got 'TextIO' instead
                if debug:
                    log.debug(SETTINGS_JSON_PATH)
                    log.debug(Utils.read_from_json(SETTINGS_JSON_PATH))
                return True
        except FileNotFoundError:
            log.error('file %r not write because not file', filepath)
        except json.JSONDecodeError:
            log.exception('file %r not write because error while decoding', filepath)
        except:
            log.exception('unknown error reading file %r', filepath)
        return False

    @staticmethod
    def update_to_json(filepath:str, data:dict) -> bool:
        exist_data = Utils.read_from_json(filepath)
        if not exist_data:
            log.warning('no current data for file %r', filepath)

        try:
            Utils.deep_update(exist_data, data)
        except:
            log.exception('unknown error while update exist data')
            return False

        if Utils.write_to_json(filepath, exist_data):
            if Utils.running: Utils.changed_links = True
            return True

        return False

    @classmethod
    def deep_update(cls, orig: dict, new: dict) -> dict:
        for key, value in new.items():
            if key in orig and isinstance(orig[key], dict) and isinstance(value, dict):
                cls.deep_update(orig[key], value)
            else:
                orig[key] = value
        return orig

    @staticmethod
    def delete_link(key:str) -> None:
        data = Utils.read_from_json(LINKS_JSON_PATH)

        if not data: log.warning('no links found')

        if key in data:
            del data[key]
            log.info('the pair %r was removed', key)
        else:
            log.info('pair %r was not saved', key)
            return

        if Utils.write_to_json(LINKS_JSON_PATH, data):
            log.info('pairs file updated')
        else:
            log.error('pair data has not been updated')

    @staticmethod
    def first_launch(date:str) -> None:
        data = Utils.read_from_json(SETTINGS_JSON_PATH)
        is_accept = data["profile"]["accept_terms_of_use"]
        if not is_accept: return

        is_launch = data["profile"]["first_launch"]
        if not is_launch and data["profile"]["id"] == 0:
            data["profile"]["first_launch"] = date
            Utils.update_to_json(SETTINGS_JSON_PATH, data)

    @staticmethod
    def get_id() -> int:
        data = Utils.read_from_json(SETTINGS_JSON_PATH)
        try:
            cur_id = int(data["profile"]["id"])
        except ValueError:
            log.debug("id is not int and that's weird")
            cur_id =  0
        except:
            cur_id = 0

        if cur_id == 0:
            cur_id = Utils.generate_id()
            data["profile"]["id"] = cur_id
            Utils.update_to_json(SETTINGS_JSON_PATH, data)

        return cur_id

    @classmethod
    def generate_id(cls) -> int:
        exist_ids = requests.get('https://jamesolson.pythonanywhere.com/keys')
        if not exist_ids: return 0
        tries = 2000

        while tries > 0:
            temp = random.randint(1, 5000)
            if not temp in exist_ids: return temp
            tries -= 1

        return 0

    @staticmethod
    def activity_app(start: str, end: str, date: str, from_:str, auto_power_off=None, auto_run=None):
        is_accept = Utils.read_from_json(SETTINGS_JSON_PATH)["profile"]["accept_terms_of_use"]
        if not is_accept: return

        id_ = Utils.get_id()
        if not start.strip() or not end.strip(): return
        url = "https://jamesolson.pythonanywhere.com/activity"
        data = {"id": str(id_), "date": date, "start": start, "end": end, "auto_power_off": auto_power_off,
                "auto_run": auto_run, "from": from_, "version": VERSION}

        requests.post(url, json=data)


    async def get_kyiv_now(self, format_datetime=False) -> str | datetime:
    
        log.info('Kyiv time request...')
    

        if self._cached_time and self._last_fetched and datetime.now(UTC) - self._last_fetched < timedelta(minutes=1):
            log.debug('using cached time')
            if format_datetime:
                return datetime.strptime(self._cached_time, "%Y-%m-%d %H:%M:%S")
            return self._cached_time
    
        url = (f'http://api.timezonedb.com/v2.1/get-time-zone?'
               f'key={os.getenv("TOKEN_TIMEZONE")}&format=json&by=zone&zone=Europe/Kyiv')
        try:
            async with aiohttp.ClientSession() as session:
                response = await session.get(url)
                today = datetime.today()

                log.debug('a request for the exact time has been sent...')
                # check status and response
                if response.status == 200 and response.content_type == 'application/json':
                    data = await response.json()
                    if data['status'] == 'OK':
                        log.info('Kyiv time was received')
                        self._cached_time = data['formatted']
                        self._last_fetched = datetime.now(UTC)
    
                        if format_datetime:
                            return datetime.strptime(self._cached_time, "%Y-%m-%d %H:%M:%S")
                        return self._cached_time
                    else:
                        log.warning('received an error from API: %s', data['status'])
                        log.error(data)
                        log.warning('use device time...')

                        if format_datetime:
                            return today
                        return today.strftime("%Y-%m-%d %H:%M:%S")

                else:
                    text = await response.text()
                    log.warning('%s server response', response.status)
                    log.debug('response:\n%s', text)

                    log.warning('use device time...')

                    if format_datetime:
                        return today
                    return today.strftime("%Y-%m-%d %H:%M:%S")
    
        except Exception:
            log.exception('unknown error when obtaining accurate Kyiv time')
    
        # Фолбэк: если ничего не вышло, возвращаем кеш, если он есть
        if self._cached_time:
            log.info('return cached time')
            if format_datetime:
                return datetime.strptime(self._cached_time, "%Y-%m-%d %H:%M:%S")
            return self._cached_time
        else:
            if format_datetime:
                return today
            return today.strftime("%Y-%m-%d %H:%M:%S")
    
