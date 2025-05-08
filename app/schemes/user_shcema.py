from pydantic import BaseModel
from app.core.settings import SETTINGS_JSON_PATH
from app.core.utils import Utils

class UserSchema(BaseModel):
    personal_schedule: str
    autorun: bool
    auto_off: bool
    accept_terms_of_use: bool
    login: str
    id: int
    first_launch: str
    start: str

    @classmethod
    def load(cls) -> "UserSchema":
        raw = Utils.read_from_json(SETTINGS_JSON_PATH)
        return cls(**raw.get("profile", {}))

    def save(self):
        data = {"profile": self.model_dump()}
        Utils.write_to_json(SETTINGS_JSON_PATH, data)

    def clear(self):
        self.personal_schedule = ""
        self.autorun = False
        self.auto_off = False
        self.accept_terms_of_use = False
        self.login = ""
        self.id = 0
        self.first_launch = ""
        self.start = ""
        self.save()