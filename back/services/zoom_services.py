import psutil
from selenium.webdriver.common.by import By

class ZoomServices:

    __driver = None

    def __init__(self, web_driver):
        self.__driver = web_driver

    async def join(self, url_zoom:str):
        btn_launch_xpath = '/html/body/div[2]/div[2]/div/div[1]/div'

        try:
            self.__driver.get(url_zoom)
            print('[Success]: перешли по ссылке на zoom')
        except Exception as e:
            print(f'[Error]: при заходе на zoom\n{url_zoom}\n\n{e}\n')

        try:
            self.__driver.find_element(By.XPATH, btn_launch_xpath).click()
            print('[Success]: зашли на пару')
        except Exception as e:
            print(f'[Error]: при заходе на zoom\n{e}')

    @staticmethod
    async def is_running():
        print('[Info]: пытаемся получить pid zoom...')
        for process in psutil.process_iter(['pid', 'name']):
            if process.info['name'] and 'zoom' in process.info['name'].lower():
                return process.info['pid']
        return None

    @staticmethod
    async def kill_process_tree(pid):
        try:
            parent = psutil.Process(pid)
            children = parent.children(recursive=True)  # Получаем все дочерние процессы
            for child in children:
                child.kill()
            parent.kill()

            print('[Success]: Zoom и все его дочерние процессы завершены')
        except psutil.NoSuchProcess:
            print('[Info]: Zoom уже завершен')
        except Exception as e:
            print(f'[Error]: при завершении Zoom\n\n{e}\n\n')

    async def kill(self):
        pid = await self.is_running()
        print(f'[Info]: pid zoom: {pid}')
        if pid:
            print('[Info]: пытаемся уничтожить процесс Zoom')
            await self.kill_process_tree(pid)
        else:
            print('[Info]: Zoom не запущен')