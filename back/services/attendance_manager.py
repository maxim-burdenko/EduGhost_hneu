import asyncio
from datetime import datetime
from back.utils import send_message_to_user
from back.settings import TIMEZONE

class AttendanceManager:
    """
    Главный менеджер класса, координирующий проставки отметки
    и участие в Zoom-встречах
    """

    def __init__(self, pns_service, zoom_service, links: dict, schedule_service = None, custom_schedule= None):
        self.pns = pns_service
        self.zoom = zoom_service
        self.schedule = schedule_service
        self.custom_schedule = custom_schedule

        self.links = links

        if self.schedule:
            self.daily_schedule = self.schedule.generate_schedule()
        else:
            self.daily_schedule = self.custom_schedule.generate_custom_schedule()

        # self.daily_schedule = \
        #     [{'subject': 'Тренінг-курс «Безпека життєдіяльності та охорона праці»', 'type': 'практ.зан.', 'start': '19:26', 'end': '19:28'},
        #     {'subject': 'ОСНОВИ МІЖНАРОДНИХ ЕКОНОМІКИ ТА МЕНЕДЖМЕНТУ', 'type': 'практ.зан.', 'start': '20:55', 'end': '23:59'}]

    def _check_time_last_lesson(self):
        last_end_time = self.daily_schedule[-1]['end']

        end = TIMEZONE.localize(datetime.combine(
            datetime.today(),
            datetime.strptime(last_end_time, "%H:%M").time()
        ))
        now = datetime.now(TIMEZONE)

        return now > end

    async def process_attendance(self):
        print('[Info]: работаем с отметкой')

        if not self.daily_schedule:
            await asyncio.sleep(2)
            send_message_to_user('Пар на сьогодні немає, відпочиваємо')
            print("[Info]: сегодня нет пар, отдыхаем")
            return

        if self._check_time_last_lesson():
            await asyncio.sleep(2)
            send_message_to_user('Усі пари закінчились, скрипт зупинено')
            print('[Info]: все пары окончены')
            return

        is_log_pns = await self.pns.login()

        for lesson in self.daily_schedule:

            if not lesson['subject'] in self.links:
                print('[Info]: ссылки не было в списке')
                continue

            now = datetime.now(TIMEZONE)
            start = TIMEZONE.localize(datetime.combine(
                datetime.today(),
                datetime.strptime(lesson["start"], "%H:%M").time()
            ))
            end = TIMEZONE.localize(datetime.combine(
                datetime.today(),
                datetime.strptime(lesson["end"], "%H:%M").time()
            ))

            if start < now < end and is_log_pns:
                print(f'[Info]: пытаемся отметится на "{lesson['subject']}"...')
                send_message_to_user(f'Спробуємо поставити відмітку на "{lesson['subject']}"')

                try:
                    if lesson["type"] == "лекція":
                        visiting_link = self.links[lesson["subject"]]["lecture"]["visiting"]
                        await self.pns.put_a_mark(visiting_link)
                    elif lesson["type"] == "лаб.зан.":
                        visiting_link = self.links[lesson["subject"]]["laboratory"]["visiting"]
                        await self.pns.put_a_mark(visiting_link)
                    elif lesson["type"] == "практ.зан.":
                        visiting_link = self.links[lesson["subject"]]["practice"]["visiting"]
                        await self.pns.put_a_mark(visiting_link)
                    else:
                        print('[Error]: не понятен тип занятия')
                        send_message_to_user(f'Не зрозумілий тип посилання на "{lesson["subject"]}"')
                except KeyError:
                    print('[Info]: ссылка не была найдена')
                    send_message_to_user("Посилання для цього заняття не було додано")
                    continue
                except Exception as e:
                    print(f'[Error]: при поиске ссылок\n{e}\n\n')
                    continue
            elif now < start and is_log_pns:
                difference = start - now
                seconds_left = int(difference.total_seconds()) + 10

                print(f'[Info]: попытаемся отметиться на паре через {seconds_left} секунд')
                print(f'[Info]: ждём начала пары...')
                send_message_to_user(f"Спробуємо відмітитись через {seconds_left} секунд")

                await asyncio.sleep(seconds_left)

                try:
                    if lesson["type"] == "лекція":
                        visiting_link = self.links[lesson["subject"]]["lecture"]["visiting"]
                        await self.pns.put_a_mark(visiting_link)
                    elif lesson["type"] == "лаб.зан.":
                        visiting_link = self.links[lesson["subject"]]["laboratory"]["visiting"]
                        await self.pns.put_a_mark(visiting_link)
                    elif lesson["type"] == "практ.зан.":
                        visiting_link = self.links[lesson["subject"]]["practice"]["visiting"]
                        await self.pns.put_a_mark(visiting_link)
                    else:
                        print('[Error]: не понятен тип занятия')
                        send_message_to_user(f'Не зрозумілий тип посилання на "{lesson["subject"]}"')
                        continue
                except KeyError:
                    print('[Info]: ссылка не была найдена')
                    continue
                except Exception as e:
                    print(f'[Error]: при поиске ссылок\n{e}\n\n')
                    continue
            elif now > end and is_log_pns:
                print(f'[Info]: пара "{lesson['subject']}" пропущена')
                send_message_to_user(f'"{lesson['subject']}" було пропущено')
                continue
            else:
                print('[Info]: не прошло время, предположительно ошибка в pns')
                continue

            now = datetime.now(TIMEZONE)
            to_end_couple = int((end - now).total_seconds()) - 300 # -5 минут (- 300)

            await asyncio.sleep(to_end_couple)

    async def process_zoom(self):
        print('[Info]: работаем с Zoom...')

        if not self.daily_schedule: return #  расписание нет, лог об этом в attendance

        if self._check_time_last_lesson(): return # все пары закончены, лог об этом в attendance

        for lesson in self.daily_schedule:
            now = datetime.now(TIMEZONE)
            start = TIMEZONE.localize(datetime.combine(
                datetime.today(),
                datetime.strptime(lesson["start"], "%H:%M").time()
            ))
            end = TIMEZONE.localize(datetime.combine(
                datetime.today(),
                datetime.strptime(lesson["end"], "%H:%M").time()
            ))

            if not lesson['subject'] in self.links: continue

            if start < now < end:
                print(f'[Info]: пара "{lesson['subject']}" уже начата')
                print(f'[Info]: пытаемся войти в zoom...')

                if lesson["type"] == "лекція":
                    zoom_link = self.links[lesson["subject"]]["lecture"]["zoom"]

                    if not zoom_link:
                        print('[Info]: ссылки Zoom не было найдено для лекции')
                        print(f'[Info]: тогда пропускаем "{lesson['subject']}"')
                        send_message_to_user(f'Не знайдено посилання zoom для пари {lesson['subject']}')
                        await asyncio.sleep(1)
                        send_message_to_user(f'Не заходимо на конференцію Zoom')
                        continue

                    await self.zoom.join(zoom_link)
                elif lesson["type"] == "лаб.зан.":
                    zoom_link = self.links[lesson["subject"]]["laboratory"]["zoom"]

                    if not zoom_link:
                        print('[Info]: ссылки Zoom не было найдено для лабораторной')
                        print(f'[Info]: тогда пропускаем "{lesson['subject']}"')
                        continue

                    await self.zoom.join(zoom_link)
                else:
                    zoom_link = self.links[lesson["subject"]]["practice"]["zoom"]

                    if not zoom_link:
                        print('[Info]: ссылки Zoom не было найдено для практической')
                        print(f'[Info]: тогда пропускаем "{lesson['subject']}"')
                        continue

                    await self.zoom.join(zoom_link)
            elif now < start:
                difference = start - now
                seconds_left = int(difference.total_seconds())

                print(f'[Info]: сейчас {now.strftime("%H:%M")}')
                print(f'[Info]: до пары "{lesson['subject']}" осталось {seconds_left} секунд')
                print(f'[Info]: ждём начала пары...')

                await asyncio.sleep(seconds_left)
                print(f'[Info]: пара началась')
                send_message_to_user(f'Пара "{lesson['subject']}" почалася')
                await asyncio.sleep(1)
                send_message_to_user('Намагаємося увійти до Zoom-конференції...')

                try:
                    if lesson["type"] == "лекція":
                        zoom_link = self.links[lesson["subject"]]["lecture"]["zoom"]

                        if not zoom_link:
                            print('[Info]: ссылки Zoom не было найдено для лекции')
                            print(f'[Info]: тогда пропускаем "{lesson['subject']}"')
                            continue

                        await self.zoom.join(zoom_link)
                    elif lesson["type"] == "лаб.зан.":
                        zoom_link = self.links[lesson["subject"]]["laboratory"]["zoom"]

                        if not zoom_link:
                            print('[Info]: ссылки Zoom не было найдено для лабораторной')
                            print(f'[Info]: тогда пропускаем "{lesson['subject']}"')
                            continue

                        await self.zoom.join(zoom_link)
                    else:
                        zoom_link = self.links[lesson["subject"]]["practice"]["zoom"]

                        if not zoom_link:
                            print('[Info]: ссылки Zoom не было найдено для практической')
                            print(f'[Info]: тогда пропускаем "{lesson['subject']}"')
                            continue

                        await self.zoom.join(zoom_link)
                except KeyError:
                    print('[Info]: ссылка не была найдена')
                    continue
                except Exception as e:
                    print(f'[Error]: при поиске ссылок\n{e}\n\n')
                    continue
            else:
                print(f'[Info]: пара "{lesson["subject"]}" пропущена')
                continue

            now = datetime.now(TIMEZONE)
            to_end_couple = int((end - now).total_seconds())  #- 600

            if to_end_couple < 0: continue

            print(f'[Info]: сейчас {now.strftime("%H:%M")}')
            print(f'[Info]: до окончания "{lesson["subject"]}" осталось {to_end_couple} секунд')
            print(f'[Info]: ждём окончание пары...')

            await asyncio.sleep(to_end_couple)

            try:
                await self.zoom.kill()
            except Exception as e:
                print(f'[Error]: при уничтожение процесса zoom\n\n{e}\n\n')