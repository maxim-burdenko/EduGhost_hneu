import asyncio
import time

from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from back import settings as s
from back.utils import send_message_to_user


class PnsServices:

    __driver = None
    __bs = None
    __isLogin = False
    __username = ""
    __password = ""

    def __init__(self, web_driver, bs, username:str, password:str):
        self.__driver = web_driver
        self. __username = username
        self.__password = password
        self.__bs = bs

    async def login(self):
        if not self.__bs.is_driver_available():
            print('[Info]: драйвер не был получен')
            return

        if self.__isLogin:
            print('[Info]: вход был выполнен')
            return

        send_message_to_user('Спроба увійти на PNS...')
        print('[Info]: пытаемся войти на PNS...')
        try:
            self.__driver.get(s.PNS_LOGIN_URL)
        except Exception as e:
            print(f'[Error]: при попытке перейти на страницу входа\n\n{e}\n\n')

        await asyncio.sleep(3)

        try:
            self.__driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(self.__username)
            await asyncio.sleep(2)
        except Exception as e:
            print(f'[Error]: при отправке логина\n\n{e}\n\n')

        try:
            self.__driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(self.__password + Keys.RETURN)
            await asyncio.sleep(2)
        except Exception as e:
            send_message_to_user('Не вдалося увійти на PNS')
            print(f'[Error]: при отправке пароля и входа\n\n{e}\n\n')

        self.__isLogin = await self._is_login()
        
        if self.__isLogin:
            send_message_to_user('Успішно зайшли на PNS')
            print('[Success]: вошли в PNS')
        else:
            send_message_to_user('Не вдалося увійти до PNS\nневінрий логін або пароль')
            print('[info]: не удалось войти в PNS')

        return self.__isLogin

    async def put_a_mark(self, url_attendance:str):
        is_link = True

        try:
            self.__driver.get(url_attendance)
        except Exception as e:
            print(f'[Error]: при переходе на отметку\n{url_attendance}\n\n{e}\n')

        try:
            link = self.__driver.find_element(By.LINK_TEXT, "Відправити відвідуваність")
            link.click()
        except NoSuchElementException:
            print('[Info]: ссылка "Відправити відвідуваність" не найдена')
            is_link = await self.re_mark(url_attendance)
        except Exception as e:
            print(f'[Error]: при поиске ссылки "Відправити відвідуваність" \n{e}')

        if not is_link: return

        await asyncio.sleep(2)

        try:
            wait = WebDriverWait(self.__driver, 10)
            labels = wait.until(ec.presence_of_all_elements_located((By.TAG_NAME, "label")))

            for label in labels:
                try:
                    input_element = label.find_element(By.TAG_NAME, "input")
                    span_element = label.find_element(By.TAG_NAME, "span")

                    if span_element.text.strip() == "Присутній":
                        input_element.click()
                        break
                except NoSuchElementException:
                    continue
                except Exception as e:
                    print(f'[Error]: при обработке label\n\n{e}\n')

            await asyncio.sleep(2)

            try:
                self.__driver.find_element(By.ID, 'id_submitbutton').click()
                print('[Success]: отметка поставлена')
            except NoSuchElementException:
                print('[Error]: кнопка "id_submitbutton" не найдена')
            except Exception as e:
                print(f'[Error]: при поиске кнопки "id_submitbutton"\n\n{e}\n')
        except NoSuchElementException:
            print('[Error]: не удалось найти labels')
        except Exception as e:
            print(f'[Error]: функция put_a_mark\n\n{e}\n')

    async def re_mark(self, url:str):
        attempt = 1

        while attempt < 5:
            attempt += 1

            print('[Info]: попытаемся отметиться вновь через 15 минут')
            await asyncio.sleep(900)  # 15 минут
            self.__driver.get(url) # перезагрузка страницы
            time.sleep(3) # для полной загрузки блокируем весь поток

            print(f'[Info]: повторная попытка отметится ({attempt}/5)')

            try:
                link = self.__driver.find_element(By.LINK_TEXT, "Відправити відвідуваність")
                link.click()
                print('[Success]: ссылка "Відправити відвідуваність" найдена')
                return True
            except NoSuchElementException:
                print('[Info]: попытка неудачная, ссылки всё ещё нет')
            except Exception as e:
                print(f'[Error]: при поиске ссылки "Відправити відвідуваність" \n{e}')

        print('[Info]: не удалось найти ссылку после 5-ти попыток')
        return False

    async def _is_login(self):
        error_class = 'loginerrors'

        try:
            self.__driver.find_element(By.CLASS_NAME, error_class)
            return False
        except NoSuchElementException:
            return True
        except Exception as e:
            print(f'[Error]: при проверке входа\n{e}\n\n')