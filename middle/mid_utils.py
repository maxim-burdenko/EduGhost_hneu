from back.utils import (update_data_to_json, load_json, get_url_schedule, check_autorun, update_autorun,
                        set_personal_schedule, set_login, set_password, get_login, get_password, delete_link,
                        update_shutdown, check_shutdown)
import back.settings as s
import back.run

import eel

@eel.expose
def insert_link(data):
    return update_data_to_json(s.LINKS_JSON_PATH, data)

@eel.expose
def get_links():
    return load_json(s.LINKS_JSON_PATH)

@eel.expose
def get_personal_schedule_url():
    return get_url_schedule()

@eel.expose
def set_personal_schedule_url(data):
    return set_personal_schedule(s.SETTINGS_JSON_PATH, data)

@eel.expose
def check_autorun_py():
    return check_autorun()

@eel.expose
def check_shutdown_py():
    return check_shutdown()

@eel.expose
def set_autorun_value(value):
    return update_autorun(s.SETTINGS_JSON_PATH, value)

@eel.expose
def set_shutdown_value(value):
    return update_shutdown(s.SETTINGS_JSON_PATH, value)

@eel.expose
def start_script():
    back.run.start()

@eel.expose
def set_pns_login(login:str):
    return set_login(s.SETTINGS_JSON_PATH, login)

@eel.expose
def set_pns_password(password:str):
    return set_password(s.SETTINGS_JSON_PATH, password)

@eel.expose
def get_pns_login():
    return get_login()

@eel.expose
def check_password():
    data = get_password()
    if data:
        return True
    else:
        return False

@eel.expose
def delete_lesson(lesson_name):
    return delete_link(lesson_name)

@eel.expose
def update_custom_schedule(data:dict):
    print(data)
    return update_data_to_json(s.CUSTOM_SCHEDULE_JSON_PATH, data)