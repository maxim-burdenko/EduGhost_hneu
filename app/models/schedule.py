from app.models.lesson import Lesson

class Schedule:
    def __init__(self, lessons:list[Lesson]):
        self.lessons = lessons
