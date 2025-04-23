import os

from back import settings as s
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as Service_Firefox
from selenium.webdriver.chrome.service import Service as Service_Chrome

class BrowserServices:

    __driver = None

    def __init__(self):
        self.__service_path_firefox = os.path.join(os.path.dirname(__file__), "geckodriver.exe")
        self.__service_path_chrome = os.path.join(os.path.dirname(__file__), "chromedriver.exe")

        self.__service_firefox = Service_Firefox(executable_path=self.__service_path_firefox)
        self.__service_chrome = Service_Chrome(executable_path=self.__service_path_chrome)

        self.__options_firefox = s.firefox_options
        self.__options_chrome = s.chrome_options


    def get_driver(self, name:str):

        if self.is_browser_installed(name.lower()) and name.lower() == "firefox":
            self.__driver = webdriver.Firefox(service=self.__service_firefox, options=self.__options_firefox)
            return self.__driver
        elif self.is_browser_installed(name.lower()) and name.lower() == "chrome":
            self.__driver = webdriver.Chrome(service=self.__service_chrome, options=self.__options_chrome)
            return self.__driver
        else:
            raise TypeError (f'[Error]: браузер {name.lower()} не добавлен или он не установлен')

    def is_driver_available(self):
        return self.__driver is not None

    @staticmethod
    def is_browser_installed(browser_name):
        program_files = [os.environ.get("ProgramFiles", ""),
                         os.environ.get("ProgramFiles(x86)", ""),
                         os.environ.get("LocalAppData", "")]

        paths = {
            "chrome": r"Google\Chrome\Application\chrome.exe",
            "firefox": r"Mozilla Firefox\firefox.exe"
        }

        if browser_name not in paths:
            return False

        for base in program_files:
            if os.path.isfile(os.path.join(base, paths[browser_name])):
                return True
        return False