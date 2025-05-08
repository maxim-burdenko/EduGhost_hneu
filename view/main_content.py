import flet as ft
from viewmodel.main_content_viewmodel import MainContentViewModel
from viewmodel.user_accessibility import UserAccessibility
from view.link_view import LinkView

from app.status_handler import StatusHandler
from logger import log


class MainContentView:
    def __init__(self, page:ft.Page, show_view, show_page):
        self.viewmodel = MainContentViewModel()
        self.user_access = UserAccessibility(StatusHandler())

        self.view_link = LinkView(page)

        self.page = page
        self.show_view = show_view
        self.show_page = show_page

        self._window_accept = ft.Column(
            [
                ft.Container(
                    ft.Column(
                        [
                            ft.Text(value='УГОДА КОРИСТУВАЧА', theme_style=ft.TextThemeStyle.TITLE_LARGE, selectable=True),

                            # ===========================================================================================
                            ft.Text(value='1. INTERPRETATION AND DEFINITIONS', theme_style=ft.TextThemeStyle.TITLE_MEDIUM, selectable=True),
                            ft.Text(value='Specific terminology used in this Privacy Policy includes:', theme_style=ft.TextThemeStyle.TITLE_SMALL, selectable=True),

                            ft.Column(
                                controls=[
                                    ft.Text("• Account – a unique account created for You to access our Service.",
                                            size=16, selectable=True),
                                    ft.Text("• Affiliate – an entity under common control with Us.", size=16, selectable=True),
                                    ft.Text("• Application – refers to EduGhost.", size=16, selectable=True),
                                    ft.Text("• Company – EduGhost (\"We\", \"Us\").", size=16, selectable=True),
                                    ft.Text("• Device – any device like a computer, cellphone, or tablet.", size=16, selectable=True),
                                    ft.Text("• Personal Data – information relating to an identifiable person.",
                                            size=16, selectable=True),
                                    ft.Text("• Service – refers to the Application.", size=16, selectable=True),
                                    ft.Text("• Service Provider – a party processing data on behalf of the Company.",
                                            size=16, selectable=True),
                                    ft.Text(
                                        "• Usage Data – automatically collected data (e.g., IP address, browser type).",
                                        size=16, selectable=True),
                                    ft.Text("• You – the individual or entity using the Service.", size=16, selectable=True),
                                ],
                                spacing=5,
                            ),

                            # ===========================================================================================
                            ft.Text(value='2. DATA COLLECTION',
                                    theme_style=ft.TextThemeStyle.TITLE_MEDIUM, selectable=True),
                            ft.Text(value='We collect the following types of Usage Data:',
                                    theme_style=ft.TextThemeStyle.TITLE_SMALL, selectable=True),

                            ft.Column(
                                controls=[
                                    ft.Text("• Anonymous user activity",
                                            size=16, selectable=True),
                                ]
                            ),

                            # ========================================================================================
                            ft.Text(value='3. USE OF PERSONAL DATA',
                                    theme_style=ft.TextThemeStyle.TITLE_MEDIUM, selectable=True),
                            ft.Text(value='Personal Data is used to:',
                                    theme_style=ft.TextThemeStyle.TITLE_SMALL, selectable=True),

                            ft.Column(
                                controls=[
                                    ft.Text("• Provide and maintain the Service",
                                            size=16, selectable=True),
                                    ft.Text("• Analyze Service usage for improvements",
                                            size=16, selectable=True),
                                ]
                            ),

                            # ==========================================================================================
                            ft.Text(value='4. DATA RETENTION', theme_style=ft.TextThemeStyle.TITLE_MEDIUM, selectable=True),
                            ft.Text(value='We retain Personal Data only as long as necessary for:',
                                    theme_style=ft.TextThemeStyle.TITLE_SMALL, selectable=True),
                            ft.Column(
                                controls=[
                                    ft.Text("• Compliance with legal obligations", size=16, selectable=True),
                                    ft.Text("• Resolving disputes", size=16, selectable=True),
                                    ft.Text("• Enforcing agreements", size=16, selectable=True),
                                ]
                            ),

                            # ==========================================================================================
                            ft.Text(value='5. DATA TRANSFER', theme_style=ft.TextThemeStyle.TITLE_MEDIUM, selectable=True),
                            ft.Text(
                                value='Your information may be transferred to servers outside of your jurisdiction. We ensure:',
                                theme_style=ft.TextThemeStyle.TITLE_SMALL, selectable=True),
                            ft.Column(
                                controls=[
                                    ft.Text("• Data protection under strict standards", size=16, selectable=True),
                                    ft.Text("• Secure handling during transfer", size=16, selectable=True),
                                ]
                            ),

                            # ==========================================================================================
                            ft.Text(value='6. DELETION OF PERSONAL DATA', theme_style=ft.TextThemeStyle.TITLE_MEDIUM, selectable=True),
                            ft.Text(value='You may:', theme_style=ft.TextThemeStyle.TITLE_SMALL, selectable=True),
                            ft.Column(
                                controls=[
                                    ft.Text("• Request deletion of Your data", size=16, selectable=True),
                                ]
                            ),
                            ft.Text("Note: Some data may be retained to meet legal requirements.", size=16, selectable=True),

                            # ==========================================================================================
                            ft.Text(value='7. DISCLOSURE OF DATA', theme_style=ft.TextThemeStyle.TITLE_MEDIUM, selectable=True),
                            ft.Text(value='We may disclose Your Personal Data:',
                                    theme_style=ft.TextThemeStyle.TITLE_SMALL, selectable=True),
                            ft.Column(
                                controls=[
                                    ft.Text("• To comply with legal obligations", size=16, selectable=True),
                                    ft.Text("• To protect and defend our rights", size=16, selectable=True),
                                    ft.Text("• To investigate possible misconduct", size=16, selectable=True),
                                    ft.Text("• In connection with business transactions", size=16, selectable=True),
                                ]
                            ),

                            # ==========================================================================================
                            ft.Text(value="8. SECURITY MEASURES", theme_style=ft.TextThemeStyle.TITLE_MEDIUM, selectable=True),
                            ft.Text(value="We employ commercially reasonable safeguards, but no method is 100% secure.",
                                    size=16, selectable=True),

                            # ==========================================================================================
                            ft.Text(value="9. CHILDREN'S PRIVACY", theme_style=ft.TextThemeStyle.TITLE_MEDIUM, selectable=True),
                            ft.Text(
                                value="We do not knowingly collect data from individuals under 13. Parental consent is required where applicable.",
                                size=16, selectable=True),

                            # ==========================================================================================
                            ft.Text(value="10. THIRD-PARTY LINKS", theme_style=ft.TextThemeStyle.TITLE_MEDIUM, selectable=True),
                            ft.Text(
                                value="Our Service may link to external sites. We are not responsible for their privacy practices.",
                                size=16, selectable=True),

                            # ==========================================================================================
                            ft.Text(value="11. POLICY UPDATES", theme_style=ft.TextThemeStyle.TITLE_MEDIUM, selectable=True),
                            ft.Text(
                                value="Privacy Policy updates will be posted here. You are advised to review it periodically.",
                                size=16, selectable=True),

                            # ==========================================================================================
                            ft.Text("12. CONTACT INFORMATION", theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
                            ft.Text("For inquiries, contact us at:", theme_style=ft.TextThemeStyle.TITLE_SMALL),
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        spans=[
                                            ft.TextSpan("• Email: "),
                                            ft.TextSpan(
                                                "maxim.burdenko2@gmail.com",
                                                style=ft.TextStyle(color=ft.colors.GREEN_400,
                                                                   decoration=ft.TextDecoration.UNDERLINE),
                                                url="mailto:maxim.burdenko2@gmail.com"
                                            )
                                        ]
                                    ),
                                    ft.Text(
                                        spans=[
                                            ft.TextSpan("• Website: "),
                                            ft.TextSpan(
                                                "https://maxim-burdenko.github.io/page_hneu.EduGhost/",
                                                style=ft.TextStyle(color=ft.colors.GREEN_400,
                                                                   decoration=ft.TextDecoration.UNDERLINE),
                                                url="https://maxim-burdenko.github.io/page_hneu.EduGhost/"
                                            )
                                        ]
                                    )
                                ]
                            ),

                            # ==========================================================================================
                            ft.Text(
                                value='WARNING: Violation of these terms may result in restricted access or legal action.',
                                theme_style=ft.TextThemeStyle.LABEL_MEDIUM
                            )

                        ],
                    ),
                    alignment=ft.alignment.top_center
                ),
                ft.Row(
                    [
                        ft.ElevatedButton(
                            content=ft.Row([
                                ft.Icon(name=ft.Icons.EXIT_TO_APP_ROUNDED, color="#FF0000"),
                                ft.Text("ВІДХИЛИТИ", color="#FF0000"),
                            ]),
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=5),
                            ),
                            on_click=lambda e: self.disable_terms(),
                        ),
                        ft.ElevatedButton(
                            content=ft.Row([
                                ft.Icon(name=ft.Icons.CHECK_ROUNDED, color="#00FF00"),
                                ft.Text('ПРИЙНЯТИ', color="#00FF00")
                            ]),
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=5),
                            ),
                            on_click= lambda e: self.accept_terms()
                        )
                    ],
                    alignment=ft.alignment.bottom_center
                )

            ],
            scroll=ft.ScrollMode.ALWAYS,
            spacing=20
        )

        self.status_text = ft.Text('неактивний', selectable=True)

        self.row_up = ft.Row(
            [
                ft.Row([
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(name=ft.Icons.PLAY_ARROW_SHARP, color="#00FF00"),
                            ft.Text('ЗАПУСТИТИ', color="#F2F3F4")
                        ]),
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=5),
                        ),
                        tooltip='Прервати роботу застосунку',
                        on_click=self.viewmodel.on_start
                    ),
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(name=ft.Icons.PAUSE_SHARP, color="#FF0000"),
                            ft.Text('ЗУПИНИТИ', color="#F2F3F4")
                        ]),
                        tooltip='Розпочати роботу застосунку',
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=5),
                        ),
                        on_click=self.viewmodel.on_stop
                    )
                ]),
                self.status_text
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        self.user_access.bind_to_view(self.update_view)

    def update_view(self, new_status: str):
        self.status_text.value = new_status
        self.page.update()



    @property
    def window_accept(self):
        return self._window_accept

    @property
    def status_accept(self):
        return self.viewmodel.get_status_accept

    @property
    def status_autostart(self):
        return  self.viewmodel.user.autorun

    def disable_terms(self):
        self.viewmodel.user.accept_terms_of_use = False
        self.viewmodel.user.save()

        self.page.window.destroy()

    def accept_terms(self):
        self.viewmodel.user.accept_terms_of_use = True
        self.viewmodel.user.save()

        self.page.clean()
        self.show_page(main=self.main_content_view())

    def main_content_view(self):

        list_lesson = []

        keys = self.viewmodel.get_key_lesson()
        for i, pair in enumerate(keys):
            # Determine background color based on index (alternating colors)
            bg_color = '#3d2b1f' if i % 2 == 0 else '#013220'

            list_lesson.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text(pair, size=16, selectable=True, expand=True, color="fffff0"),

                            # Edit Button (wrapped)
                            ft.Container(
                                content=ft.IconButton(
                                    icon=ft.icons.CREATE,
                                    icon_color="#fffdd0",
                                    tooltip="Редагувати",
                                    on_click=lambda e, p=pair: edit_pair(p),
                                    style=ft.ButtonStyle(padding=0),  # remove internal padding
                                ),
                                alignment=ft.alignment.center,
                                height=40,  # optional: match button height
                            ),

                            # Delete Button (wrapped)
                            ft.Container(
                                content=ft.IconButton(
                                    icon=ft.icons.DELETE_FOREVER,
                                    tooltip="Видалити",
                                    icon_color="#fffdd0",
                                    on_click=lambda e, p=pair: delete_pair(p),
                                    style=ft.ButtonStyle(padding=0),
                                ),
                                alignment=ft.alignment.center,
                                height=40,
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    bgcolor=bg_color,
                    border_radius=8,
                    padding=10,
                    margin=ft.margin.only(bottom=5),
                    height=50,
                )
            )

        box = ft.Column(
            controls=list_lesson,
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )

        def delete_pair(key):
            self.viewmodel.delete_lesson(key)

            for item in list_lesson:
                if isinstance(item.content, ft.Row):
                    row_controls = item.content.controls
                    if row_controls and isinstance(row_controls[0], ft.Text) and row_controls[0].value == key:
                        list_lesson.remove(item)
                        break

            box.controls = list_lesson
            self.page.update()

        def edit_pair(key):
            main = self.view_link.edit_lesson(key)

            self.page.clean()
            self.show_page(main=main)



        return ft.Container(
            alignment=ft.alignment.top_left,
            content=ft.Column(
                [
                    self.row_up,
                    box
                ],
                spacing=20
            ),
            expand=True
        )