import ctypes
import os
import shutil
import sys


from selenium.webdriver.firefox.options import Options as FirefoxOptions

from logger import log

def get_runtime_path(relative_path: str) -> str:
    """Получаем путь к ресурсу внутри PyInstaller, или к исходникам в dev-среде."""
    if getattr(sys, 'frozen', False):  # если запущено как .exe
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_user_data_path(filename: str) -> str:
    """Путь к пользовательской копии файла для записи (в %APPDATA%)."""
    app_data_dir = os.path.join(os.getenv("APPDATA"), "EduGhost")
    os.makedirs(app_data_dir, exist_ok=True)
    return os.path.join(app_data_dir, filename)

def ensure_user_file_exists(source_relative_path: str, dest_filename: str):
    """Копирует файл из bundled в пользовательскую папку, если он там не существует."""
    user_file_path = get_user_data_path(dest_filename)
    if not os.path.exists(user_file_path):
        shutil.copy(get_runtime_path(source_relative_path), user_file_path)
    return user_file_path

VERSION = "0.2.0"

PNS_LOGIN_URL = 'https://pns.hneu.edu.ua/login/index.php'
MAIN_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ICON = ensure_user_file_exists('view/icons/icon.png', 'icon.png')
FONT_3270_REGULAR = ensure_user_file_exists("view/fonts/3270-Regular.ttf", "3270-Regular.ttf")
LINKS_JSON_PATH = ensure_user_file_exists("app/data/links.json", "links.json")
SETTINGS_JSON_PATH = ensure_user_file_exists("app/data/settings.json", "settings.json")

CUSTOM_SCHEDULE_JSON_PATH = os.path.join(BASE_DIR, "data", "custom_schedule.json")
PATH_ENV =  os.path.join(BASE_DIR, ".env")

DRIVER_FIREFOX_PATH = os.path.join(BASE_DIR, 'drivers', 'geckodriver.exe')



ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001

FONTS_PATH = os.path.join(MAIN_DIR, "view", "fonts")
# FONT_3270_REGULAR = os.path.join(FONTS_PATH, "3270-Regular.ttf")
# LINKS_JSON_PATH = os.path.join(BASE_DIR, "data", "links.json")
# SETTINGS_JSON_PATH = os.path.join(BASE_DIR, "data", "settings.json")

firefox_paths = [
    r'C:\Program Files (x86)\Mozilla Firefox',
    r'C:\Program Files\Mozilla Firefox'
]

firefox_binary = r''

for path in firefox_paths:
    if os.path.exists(path):
        firefox_binary = path

if firefox_binary:
    firefox_binary += r'\firefox.exe'

# Настройки FireFox для автоматического входа на конференцию
firefox_options = FirefoxOptions()
firefox_options.set_preference("network.protocol-handler.external.zoommtg", True)
firefox_options.set_preference("network.protocol-handler.expose.zoommtg", True)
firefox_options.set_preference("network.protocol-handler.warn-external.zoommtg", False)
firefox_options.add_argument("--headless") # без GUI по
firefox_options.binary_location = firefox_binary



def prevent_sleep():
    """Prevent Windows from sleeping while the script is running."""
    ctypes.windll.kernel32.SetThreadExecutionState(
        ES_CONTINUOUS | ES_SYSTEM_REQUIRED
    )
    log.info('запобігання сну включено')

def allow_sleep():
    """Allow Windows to sleep normally again."""
    ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
    log.info('запобігання сну вимкнено — система працює штатно')


MONTHS_UK = {
    "January": "січня", "February": "лютого", "March": "березня",
    "April": "квітня", "May": "травня", "June": "червня",
    "July": "липня", "August": "серпня", "September": "вересня",
    "October": "жовтня", "November": "листопада", "December": "грудня"
}

MAPPED_TYPE_LESSON = {
    "лекція": "lecture",
    "практ.зан.": "practice",
    "лаб.зан.": "laboratory"
}
