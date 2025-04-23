import ctypes

import pytz
import os
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions



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

chrome_options = ChromeOptions()

prefs = {
    "protocol_handler.allowed_origin_protocol_pairs": {
        "https://us02web.zoom.us": ["zoommtg"]
    }
}

chrome_options.add_experimental_option("prefs", prefs)

#chrome_options.add_argument("--headless=new")  # gui
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

TIMEZONE = pytz.timezone('Europe/Kyiv')
PNS_LOGIN_URL = 'https://pns.hneu.edu.ua/login/index.php'

ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002

def prevent_sleep():
    """Prevent Windows from sleeping while the script is running."""
    ctypes.windll.kernel32.SetThreadExecutionState(
        ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED
    )
    print('[Info]: включено предотвращение сна')

def allow_sleep():
    """Allow Windows to sleep normally again."""
    ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
    print('[Info]: предотвращение сна отключено — система работает штатно')

MONTHS_UK = {
    "January": "січня", "February": "лютого", "March": "березня",
    "April": "квітня", "May": "травня", "June": "червня",
    "July": "липня", "August": "серпня", "September": "вересня",
    "October": "жовтня", "November": "листопада", "December": "грудня"
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LINKS_JSON_PATH = os.path.join(BASE_DIR, "data", "links.json")
SETTINGS_JSON_PATH = os.path.join(BASE_DIR, "data", "settings.json")
CUSTOM_SCHEDULE_JSON_PATH = os.path.join(BASE_DIR, "data", "custom_schedule.json")
