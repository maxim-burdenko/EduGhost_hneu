import json
import os
from typing import TextIO

from back import settings
import eel


def load_json(filepath: str) -> dict:
    """Загружает данные из JSON файла."""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            if not content.strip():  # Проверяем, пуст ли файл
                raise ValueError("файл пуст")
            return json.loads(content)
    except FileNotFoundError:
        print(f'[Error]: файл "{filepath}" не найден.\n')
    except json.JSONDecodeError as e:
        print(f'[Error]: ошибка декодирования JSON\n\n{e}\n\n')
    except ValueError as e:
        print(f'[Error]: {e}\n')
    except Exception as e:
        print(f'[Error]: неизвестная ошибка\n\n{e}\n\n')

    return {}

def update_data_to_json(filepath: str, data: dict):
    """Добавляем данные ссылок в JSON файл."""
    try:
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                existing_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = {}

        existing_data.update(data)

        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(json.dumps(existing_data, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f'[Error]: при вставке данных в JSON\n\n{e}\n\n')

def insert_data_to_json(filepath: str, data: dict):
    """Перезаписываем JSON-файл с новыми данными."""
    try:
        json_data = json.dumps(data, indent=2, ensure_ascii=False)
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(json_data)
    except Exception as e:
        print(f'[Error]: при вставке данных в JSON\n\n{e}\n\n')

def get_url_schedule():
    data = load_json(settings.SETTINGS_JSON_PATH)
    url = data["profile"]["personal_schedule"]
    settings.SCHEDULE_URL = url
    return url

def check_autorun():
    data = load_json(settings.SETTINGS_JSON_PATH)
    is_autorun = data["profile"]["autorun"]

    return is_autorun

def update_autorun(filepath: str, autorun_value: bool):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if 'profile' in data:
            data['profile']['autorun'] = autorun_value

        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(json.dumps(data, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f'[Error]: при обновлении авто-запуска\n\n{e}\n\n')

def set_personal_schedule(filepath: str, url: str):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if 'profile' in data:
            data['profile']['personal_schedule'] = url

        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(json.dumps(data, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f'[Error]: при обновлении личного расписания\n\n{e}\n\n')


def set_login(filepath, login:str):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if 'profile' in data:
            data['profile']['login'] = login

        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(json.dumps(data, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f'[Error]: при обновлении логина\n\n{e}\n\n')

def set_password(filepath, password:str):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if 'profile' in data:
            data['profile']['password'] = password

        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(json.dumps(data, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f'[Error]: при обновлении пароля\n\n{e}\n\n')

def get_password():
    data = load_json(settings.SETTINGS_JSON_PATH)
    return data["profile"]["password"]

def get_login():
    data = load_json(settings.SETTINGS_JSON_PATH)
    return data["profile"]["login"]

def delete_link(key_to_delete):
    data = load_json(settings.LINKS_JSON_PATH)

    if not data: print('[Info]: ссылок нету')

    print(key_to_delete)

    if key_to_delete in data:
        del data[key_to_delete]
        print('[Success]: ссылка была удалена')

    insert_data_to_json(settings.LINKS_JSON_PATH, data)
    print('[Success]: файл с ссылками был обновлён')

def check_custom_schedule():
    data = load_json(settings.SETTINGS_JSON_PATH)

    return data["profile"]["customSchedule"]

def import_data(data: dict, type_data:str='settings'):
    if type_data == 'settings':

        if 'profile' not in data:
            print("[Error]: Ключ 'profile' не найден в данных")
            print('[Info]: никаких изменений внесено не было')
            return

        profile = data['profile']

        required_keys = {
            'personal_schedule': 'https://',
            'autorun': False,
            'shutdown': False,
            'login': '',
            'password': ''
        }

        for key, default_value in required_keys.items():
            if key not in profile:
                profile[key] = default_value
                print(f"[Info]: Ключ '{key}' не найден. Добавлен со значением по умолчанию: {default_value}")

        file_path = settings.SETTINGS_JSON_PATH

        if not os.path.exists(file_path):
            print("[Info]: Файл 'settings.json' не найден. Будет создан новый файл.")

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump({'profile': profile}, f, ensure_ascii=False, indent=2)
            print("[Info]: Данные сохранены в 'settings.json'")
    elif type_data == 'links':

        if not data: print('[Info]: данные ссылок были пусты, ничего не меняем'); return

        updated = False
        structure_template = {
            "lecture": {"zoom": "", "visiting": ""},
            "practice": {"zoom": "", "visiting": ""},
            "laboratory": {"zoom": "", "visiting": ""}
        }

        for subject, content in data.items():
            if not isinstance(content, dict):
                print(f"[Warning]: Значение по ключу '{subject}' не является словарём. Пропускаем.")
                continue

            for part, fields in structure_template.items():
                if part not in content:
                    content[part] = fields.copy()
                    print(f"[Info]: Для '{subject}' добавлен раздел '{part}' со значениями по умолчанию.")
                    updated = True
                else:
                    for field_key, default_value in fields.items():
                        if field_key not in content[part]:
                            content[part][field_key] = default_value
                            print(f"[Info]: В '{subject}' > '{part}' добавлено поле '{field_key}' со значением по умолчанию: {default_value}")
                            updated = True

        file_path = settings.LINKS_JSON_PATH

        if not os.path.exists(file_path):
            print("[Info]: Файл 'links.json' не найден. Будет создан новый файл.")

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            print("[Info]: Данные сохранены в 'links.json'")


    else:
        print('[Info]: данные для импорта не понятны')
        return

def check_shutdown():
    data = load_json(settings.SETTINGS_JSON_PATH)
    return data["profile"]["shutdown"]

def update_shutdown(filepath: str, autorun_value: bool):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if 'profile' in data:
            data['profile']['shutdown'] = autorun_value

        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(json.dumps(data, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f'[Error]: при обновлении авто-завершения\n\n{e}\n\n')

def change_status_to_user(status:str, color:str):
    return eel.changeStatus(status, color)

def send_message_to_user(message:str):
    return eel.sendMessageToUser(message)