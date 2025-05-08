import flet as ft
from view.main_content import MainContentView
from view.profile_view import ProfileView
from view.link_view import LinkView
from app.core.settings import FONT_3270_REGULAR, ICON
from app.run import stop, start
import asyncio


class MainWindow:
    def __init__(self, page:ft.Page):
        self.page = page

        self.page.title = "EduGhost"
        self.page.horizontal_alignment = "stretch"
        self.page.vertical_alignment = "start"

        self.page.window.width = 960
        self.page.window.height = 580
        self.page.window.top = 100
        self.page.window.left = 100
        self.page.bgcolor = "#0A0F0F"

        self.page.fonts = {
            "3270-Regular": FONT_3270_REGULAR
        }

        self.page.theme = ft.Theme(font_family="3270-Regular")

        self.page.update()

        self.content_view = MainContentView(self.page, self.show_view, self.show_page)
        self.profile_view = ProfileView(self.page).profile_view
        self.link_view = LinkView(self.page).link_view
        self.is_accept_terms = self.content_view.status_accept
        self.is_autostart = self.content_view.status_autostart


        self.page.on_window_event = self.on_window_close

        self.main_content = ft.Container(
            alignment=ft.alignment.top_left,
            content=MainContentView(self.page, self.show_view, self.show_page).main_content_view(),
            margin=20,
            expand=True
        )

        self.side_nav = ft.Container(
            width=220,
            bgcolor="#141A1A",
            padding=0,
            margin=-10,
            border=ft.border.only(right=ft.BorderSide(1, ft.colors.RED_ACCENT), ),
            content=ft.Column(
                controls=[
                    self.nav_item(ft.icons.HOME, "Головна", lambda e: self.show_view("home")),
                    self.nav_item(ft.icons.PERSON, "Профіль", lambda e: self.show_view("profile")),
                    self.nav_item(ft.icons.LINK, "Посилання", lambda e: self.show_view("link")),
                ],
                alignment=ft.alignment.top_left,
                spacing=10
            )
        )

        if self.is_accept_terms:

            self.show_page()
        else:
            self.main_content.content = self.content_view.window_accept
            self.page.update()

            self.show_page(with_nav=False)

        if self.is_autostart:
            asyncio.create_task(self.on_view_loaded())

    async def on_view_loaded(self, e=None):
        self.page.open(ft.SnackBar(
            content=ft.Text('Автозапуск через 15 секунд', color="#FFC300", selectable=True),
            bgcolor="#36454F",
        ))
        await asyncio.sleep(15)
        await start()

    async def on_window_close(self):
        await stop()
        await asyncio.sleep(0.1)
        self.page.window.destroy()


    def show_view(self, view_name):
        self.page.clean()
        if view_name == "home":
            self.main_content.content = MainContentView(self.page, self.show_view, self.show_page).main_content_view()
        elif view_name == "profile":
            self.main_content.content = self.profile_view
        elif view_name == 'link':
            self.main_content.content = self.link_view
        else:
            pass
        self.page.update()
        self.show_page()

    def show_page(self, main=None, with_nav=True):
        if not main:
            main = self.main_content

        if not with_nav:
            self.page.add(
                ft.Row(
                    controls=[
                        main
                    ],
                    expand=True
                )
            )
        else:
            self.page.add(
                ft.Row(
                    controls=[
                        self.side_nav,
                        main
                    ],
                    expand=True
                )
            )

    def nav_item(self, icon, text, on_click):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(icon, color="#00FF00"),
                    ft.Text(text, color="#fffff0")
                ]
            ),
            padding=15,
            margin=0,
            border_radius=5,
            ink=True,
            on_click=on_click,
            on_hover=self.handle_hover,
            tooltip=text
        )

    @staticmethod
    def handle_hover(e):
        e.control.bgcolor = "#1E2E2E" if e.data == "true" else None
        e.control.update()


 # async def on_start(_):
 #        await start()
 #
 #    async def on_stop(_):
 #        await stop()
 #
 #    async def on_window_close(_):
 #        await stop()
 #        await asyncio.sleep(0.1)
 #        page.window_destroy()
# page.on_window_event = on_window_close

# ft.ElevatedButton("Старт скрипт", on_click=on_start),
# ft.ElevatedButton("Стоп скрипт", on_click=on_stop),