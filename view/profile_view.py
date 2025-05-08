import flet as ft
from viewmodel.profile_viewmodel import ProfileViewModel
from logger import log

class ProfileView:

    def __init__(self, page:ft.Page):
        self.view_model = ProfileViewModel()
        self.page = page


    @property
    def profile_view(self):

        def info_icon(tooltip_text):
            icon = ft.Icon(ft.icons.INFO_OUTLINE, size=18, color="#00FF00")  # Using hex color instead of colors enum
            return ft.Container(
                content=icon,
                tooltip=ft.Tooltip(
                    message=tooltip_text,
                    prefer_below = False,
                ),
                padding=ft.padding.all(5)
            )

        message_url = ft.Text(
            value="",
            selectable=True,
            color=ft.Colors.RED_50,
        )

        log_pas_message = ft.Text(
            value="",
            selectable=True,
            color=ft.Colors.RED_50,
        )

        url_text_field = ft.TextField(
            label="Посилання на особистий розклад ХНЕУ",
            label_style=ft.TextStyle(color="#03c03c"),
            hint_text="http://www.rozklad.hneu.edu.ua/schedule/schedule?group=00000&student=000000",
            expand=True,
            focused_border_color="#00FF24",
            border_color="00FF24",
            color="#00FF00",
        )

        def change_status(url:str, login:str, password:str):
            info = self.view_model.add_data_profile(url, login, password)

            if not info:
                message_url.value = ""
                log_pas_message.value = ""

                url_text_field.value = ""
                login_field.value = ""
                password_field.value = ""

                update_data()
                self.page.update()
                return

            for error_type, error_msg in info:
                if error_type == "url":
                    message_url.value = error_msg
                elif error_type == "log_pass":
                    log_pas_message.value = error_msg
                else:
                    log.error('не зрозуміло для кого')

            url_text_field.value = ""
            login_field.value = ""
            password_field.value = ""

            update_data()
            self.page.update()

        url_text = ft.Text("", selectable=True)
        login_text = ft.Text("", selectable=True)
        password_text = ft.Text("", selectable=True)

        def update_data():
            url = self.view_model.get_url()
            login = self.view_model.get_login()
            password = self.view_model.get_password()

            url_text.value = f'{"Особисте посилання:":<22} {url[:11] + "..." + url[39:]}'
            login_text.value = f'{"Логін:":<22} {login[:50] + "..." if len(login) > 50 else login}'
            password_text.value = f'{"Пароль:":<22} {password[:50] + "..." if len(password) > 50 else password}'

            self.page.update()

        personal_layout_link = ft.Container(
            ft.Column([
                url_text_field,
                message_url],
            spacing=5),
            padding=ft.padding.only(left=20, top=20, right=20),
            bgcolor="#111e0b",
            border_radius=5,
        )

        login_field = ft.TextField(
            label="Логін PNS",
            label_style=ft.TextStyle(color="#03c03c"),
            hint_text="Уведіть валідний логін",
            expand=True,
            focused_border_color="#00FF24",
            border_color="00FF24",
            color="#00FF00",
        )

        password_field = ft.TextField(
            label="Пароль PNS",
            password=True,
            label_style=ft.TextStyle(color="#03c03c"),
            can_reveal_password=True,
            hint_text="Уведіть дійсний пароль",
            expand=True,
            focused_border_color="#00FF24",
            border_color="00FF24",
            color="#00FF00",
        )

        credentials_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Облікові дані доступу до PNS", weight=ft.FontWeight.BOLD),
                    login_field,
                    password_field,
                    log_pas_message,
                ], spacing=10),
                padding=15
            ),
            margin=ft.margin.only(top=10, bottom=20)
        )

        auto_start_cb = ft.Checkbox(
            label="Автоматичний запуск",
            value = self.view_model.get_autorun(),
            active_color="#00FF00",
            on_change=lambda e: self.view_model.set_autorun(e.control.value)
        )
        auto_start_info = info_icon(
            "Коли увімкнено, запуск скрипта розпочнеться автоматично через 15 секунд. Детальніше у телеграм каналі"
        )

        auto_shutdown_cb = ft.Checkbox(
            label="Автоматичне завершення роботи ПК ",
            value=self.view_model.get_auto_off(),
            active_color="#00FF00",
            on_change=lambda e: self.view_model.set_auto_off(e.control.value)
        )
        auto_shutdown_info = info_icon("Коли увімкнено, то після завершення усіх пар, "
                                       "Ваш ПК буде автоматично вимкнено через 5 хвилин.")

        save_button = ft.ElevatedButton(
            "Зберегти/Оновити",
            icon=ft.icons.SAVE,
            icon_color="#FFFFF0",
            style=ft.ButtonStyle(
                color="#FFFFF0",
                bgcolor="#6b8e23",
            ),
            on_click=lambda e: change_status(
                url_text_field.value,
                login_field.value,
                password_field.value
            ),
            expand=True
        )

        previous_settings = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            url_text,
                            login_text,
                            password_text
                        ],
                        spacing=5,
                        expand=True
                    ),
                    expand=True,
                )
            ]
        )

        warning_text = ft.Text(
            spans=[
                ft.TextSpan("\nПароль та логін для PNS потрібно для того, щоб робити відвідування від Вашого імені. Якщо Ви"),
                ft.TextSpan(" НЕ БАЖАЄТЕ ", style=ft.TextStyle(color="#00FF24", weight=ft.FontWeight.BOLD)),
                ft.TextSpan("ставити відмітки присутності на заняттях, то можете просто не вказувати ці поля.\nПароль та логін"),
                ft.TextSpan(" НЕ ПЕРЕДАЮТЬСЯ ", style=ft.TextStyle(color="#00FF24", weight=ft.FontWeight.BOLD)),
                ft.TextSpan('третім особам, ці дані зберігаються виключно на вашому пристрої')
            ],
            size=14,
            color="#19e636",
            selectable = True
        )

        update_data()

        return ft.Container(
            alignment=ft.alignment.top_left,
            content=ft.Column(
                [
                    personal_layout_link,
                    credentials_card,
                    ft.Container(
                        content=save_button,
                        alignment=ft.alignment.center,
                        margin=ft.margin.only(top=20, bottom=30)
                    ),

                    ft.Row([auto_start_cb, auto_start_info], alignment=ft.MainAxisAlignment.START),
                    ft.Row([auto_shutdown_cb, auto_shutdown_info], alignment=ft.MainAxisAlignment.START),

                    ft.Divider(height=1, color="#BDBDBD"),

                    ft.Container(
                        content=previous_settings,
                        border_radius=10,
                        padding=10
                    ),

                    ft.Divider(height=1, color="#BDBDBD"),

                    warning_text
                ],
                scroll=ft.ScrollMode.ALWAYS
            ),
            expand=True
        )