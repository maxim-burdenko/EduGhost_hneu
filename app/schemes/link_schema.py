from pydantic import BaseModel
from typing import Dict
from app.core.utils import Utils
from app.core.settings import LINKS_JSON_PATH


class ActivityLinks(BaseModel):
    zoom: str
    attendance: str

class CourseLinks(BaseModel):
    lecture: ActivityLinks
    practice: ActivityLinks
    laboratory: ActivityLinks

class LinksSchema(BaseModel):
    courses: Dict[str, CourseLinks]

    @classmethod
    def load(cls) -> "LinksSchema":
        data = Utils.read_from_json(LINKS_JSON_PATH)
        return cls(courses=data)

    def save(self):
        Utils.write_to_json(LINKS_JSON_PATH, self.model_dump())


