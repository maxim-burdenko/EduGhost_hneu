import flet as ft
from viewmodel.link_viewmodel import LinkViewModel
from logger import log

class LinkView:
    def __init__(self, page:ft.Page):
        self.view_model = LinkViewModel()
        self.page = page
        
        self.name_lesson_field = ft.TextField(
            label='Назва пари',
            label_style=ft.TextStyle(color="#03c03c"),
            focused_border_color="#00FF24",
            border_color="00FF24",
            color="#00FF00"
        )

        self.lecture_zoom_field = ft.TextField(
            label='Лекція Zoom',
            label_style=ft.TextStyle(color="#03c03c"),
            focused_border_color="#00FF24",
            border_color="00FF24",
            color="#00FF00"
        )
        self.practice_zoom_field = ft.TextField(
            label='Практична Zoom',
            label_style=ft.TextStyle(color="#03c03c"),
            focused_border_color="#00FF24",
            border_color="00FF24",
            color="#00FF00"
        )
        self.laboratory_zoom_field = ft.TextField(
            label='Лабораторна Zoom',
            label_style=ft.TextStyle(color="#03c03c"),
            focused_border_color="#00FF24",
            border_color="00FF24",
            color="#00FF00"
        )

        self.lecture_attendance_field = ft.TextField(
            label='Лекція відвідування',
            label_style=ft.TextStyle(color="#03c03c"),
            focused_border_color="#00FF24",
            border_color="00FF24",
            color="#00FF00"
        )
        self.practice_attendance_field = ft.TextField(
            label='Практична відвідування',
            label_style=ft.TextStyle(color="#03c03c"),
            focused_border_color="#00FF24",
            border_color="00FF24",
            color="#00FF00"
        )
        self.laboratory_attendance_field = ft.TextField(
            label='Лабораторна відвідування',
            label_style=ft.TextStyle(color="#03c03c"),
            focused_border_color="#00FF24",
            border_color="00FF24",
            color="#00FF00"
        )

        # ======================================================================================
        self.name_lesson_text = ft.Text(value="", size=13, selectable=True)

        self.lecture_zoom_text = ft.Text(value="", size=13, selectable=True)
        self.practice_zoom_text = ft.Text(value="", size=13, selectable=True)
        self.laboratory_zoom_text = ft.Text(value="", size=13, selectable=True)

        self.lecture_attendance_text = ft.Text(value="", size=13, selectable=True)
        self.practice_attendance_text = ft.Text(value="", size=13, selectable=True)
        self.laboratory_attendance_text = ft.Text(value="", size=13, selectable=True)

        # ====================================================================================
        self.column_name_lesson = ft.Column(
            [
                self.name_lesson_field,
                self.name_lesson_text
            ]
        )
        # ===================================================================================
        self.column_lecture_zoom = ft.Column(
            [
                self.lecture_zoom_field,
                self.lecture_zoom_text
            ]
        )
        self.column_practice_zoom = ft.Column(
            [
                self.practice_zoom_field,
                self.practice_zoom_text
            ]
        )
        self.column_laboratory_zoom = ft.Column(
            [
                self.laboratory_zoom_field,
                self.laboratory_zoom_text
            ]
        )

        # ===========================================
        self.column_lecture_attendance = ft.Column(
            [
                self.lecture_attendance_field,
                self.lecture_attendance_text
            ]
        )
        self.column_practice_attendance = ft.Column(
            [
                self.practice_attendance_field,
                self.practice_attendance_text
            ]
        )
        self.column_laboratory_attendance = ft.Column(
            [
                self.laboratory_attendance_field,
                self.laboratory_attendance_text
            ]
        )
        # =================================================================================
        self.left_column = ft.Column(
            [
                self.column_lecture_zoom,
                self.column_practice_zoom,
                self.column_laboratory_zoom
            ],
            expand=True
        )

        self.right_column = ft.Column(
    [
                self.column_lecture_attendance,
                self.column_practice_attendance,
                self.column_laboratory_attendance
            ],
            expand=True
        )
        self.row = ft.Row(
            [
                self.left_column,
                self.right_column
            ]
        )
        #======================================================================================
        self.send_button = ft.ElevatedButton(
            "Зберегти/Оновити",
            icon=ft.icons.SAVE,
            icon_color="#FFFFF0",
            style=ft.ButtonStyle(
                color="#FFFFF0",
                bgcolor="#6b8e23",
            ),
            on_click=lambda e: self.save_lesson(
                self.name_lesson_field.value,

                self.lecture_zoom_field.value,
                self.practice_zoom_field.value,
                self.laboratory_zoom_field.value,

                self.lecture_attendance_field.value,
                self.practice_attendance_field.value,
                self.laboratory_attendance_field.value,
            )
        )

        self.row_btn = ft.Row(
            [self.send_button],
            alignment=ft.MainAxisAlignment.CENTER
        )

        self.main_column = ft.Column(
            controls=[
                ft.Container(
                    ft.Text('Налаштування посилань', theme_style=ft.TextThemeStyle.TITLE_LARGE),
                    margin=ft.margin.only(bottom=20)
                ),
                self.column_name_lesson,
                self.row,
                self.row_btn
            ],
            scroll=ft.ScrollMode.ALWAYS
        )

        self.container = ft.Container(
            alignment=ft.alignment.top_left,
            content=self.main_column,
            margin=5,
            expand=True
        )


    def edit_lesson(self, key):
        lesson = self.view_model.get_lesson_by_key(key)

        if not lesson: return

        self.name_lesson_field.value = key

        self.lecture_zoom_field.value = lesson[key]["lecture"]["zoom"]
        self.practice_zoom_field.value = lesson[key]["practice"]["zoom"]
        self.laboratory_zoom_field.value = lesson[key]["laboratory"]["zoom"]

        self.lecture_attendance_field.value = lesson[key]["lecture"]["attendance"]
        self.practice_attendance_field.value = lesson[key]["practice"]["attendance"]
        self.laboratory_attendance_field.value = lesson[key]["laboratory"]["attendance"]

        self.column_name_lesson.controls[0] = self.name_lesson_field

        self.column_lecture_zoom.controls[0] = self.lecture_zoom_field
        self.column_practice_zoom.controls[0] = self.practice_zoom_field
        self.column_laboratory_zoom.controls[0] = self.laboratory_zoom_field

        self.column_lecture_attendance.controls[0] = self.lecture_attendance_field
        self.column_practice_attendance.controls[0] = self.practice_attendance_field
        self.column_laboratory_attendance.controls[0] = self.laboratory_attendance_field

        self.left_column.controls[0] = self.column_lecture_zoom
        self.left_column.controls[1] = self.column_practice_zoom
        self.left_column.controls[2] = self.column_laboratory_zoom

        self.right_column.controls[0] = self.column_lecture_attendance
        self.right_column.controls[1] = self.column_practice_attendance
        self.right_column.controls[2] = self.column_laboratory_attendance

        self.row.controls[0] = self.left_column
        self.row.controls[1] = self.right_column

        self.main_column.controls[1] = self.column_name_lesson
        self.main_column.controls[2] = self.row
        self.main_column.controls[3] = self.row_btn

        self.container.content = self.main_column
        self.page.update()
        return self.container

    def save_lesson(self, name: str, lecture_zoom: str, practice_zoom: str, laboratory_zoom: str,
                    lecture_attendance: str, practice_attendance: str, laboratory_attendance: str):

        info = self.view_model.add_lesson(name, lecture_zoom, practice_zoom, laboratory_zoom, lecture_attendance,
                                          practice_attendance, laboratory_attendance)

        if not info:
            log.debug("info було пусто")
            self.name_lesson_field.value = ""
            self.name_lesson_text.value = ""
            # =============================================================
            self.lecture_zoom_field.value = ""
            self.practice_zoom_field.value = ""
            self.laboratory_zoom_field.value = ""

            self.lecture_attendance_field.value = ""
            self.practice_attendance_field.value = ""
            self.laboratory_attendance_field.value = ""
            # ==============================================================
            self.lecture_zoom_text.value = ""
            self.practice_zoom_text.value = ""
            self.laboratory_zoom_text.value = ""

            self.lecture_attendance_text.value = ""
            self.practice_attendance_text.value = ""
            self.laboratory_attendance_text.value = ""
            self.page.update()
            return

        for type_msg, message in info:
            if type_msg == "name":
                self.name_lesson_text.value = message
            elif type_msg == "lecture_zoom":
                self.lecture_zoom_text.value = message
            elif type_msg == "practice_zoom":
                self.practice_zoom_text.value = message
            elif type_msg == "laboratory_zoom":
                self.laboratory_zoom_text.value = message
            elif type_msg == "lecture_attendance":
                self.lecture_attendance_text.value = message
            elif type_msg == "practice_attendance":
                self.practice_attendance_text.value = message
            elif type_msg == "laboratory_attendance":
                self.laboratory_attendance_text.value = message
            else:
                log.error('не зрозумілий тип повідомлення')

        self.page.update()



    @property
    def link_view(self):
        return self.container
