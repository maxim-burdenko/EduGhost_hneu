import os

from app.core import settings as s
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as Service_Firefox

class Browser:

    def __init__(self):
        self._driver = None
        self._service_path_firefox = s.DRIVER_FIREFOX_PATH
        self._service_firefox = Service_Firefox(executable_path=self._service_path_firefox)
        self._options_firefox = s.firefox_options

    @property
    async def driver(self):
        if not self._driver:
            self._driver = webdriver.Firefox(service=self._service_firefox, options=self._options_firefox)
        return self._driver

    def is_driver_available(self):
        return self._driver is not None