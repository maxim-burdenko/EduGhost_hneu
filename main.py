import asyncio

import flet as ft

from app.core.utils import Utils
from app.core.config import Config
from view.main_window import MainWindow
from app.schemes.user_shcema import UserSchema

from logger import log

async def main(page:ft.Page):
    return MainWindow(page)

if __name__ == "__main__":
    start = "99:99"
    user = UserSchema.load()
    try:
        start = asyncio.run(Utils().get_kyiv_now(format_datetime=True)).strftime('%H:%M')
        if not Config().get_password(user.login):
            user.clear()
    except:
        pass

    try:
        ft.app(target=main, assets_dir="view/icons", view=ft.FLET_APP)
    except:
        log.exception('unknown error while start/work app')
    finally:
        now = asyncio.run(Utils().get_kyiv_now(format_datetime=True))
        end = now.strftime('%H:%M')
        date = now.strftime('%d-%m-%Y')
        Utils().first_launch(date)
        Utils().activity_app(start, end ,date, "main", user.auto_off, user.autorun)
