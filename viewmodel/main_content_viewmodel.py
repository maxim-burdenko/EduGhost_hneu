from app.core.utils import Utils
from app.core.settings import LINKS_JSON_PATH
from app.schemes.user_shcema import UserSchema

from app.run import start, stop

class MainContentViewModel:
    def __init__(self):
        self.utils = Utils()
        self.user = UserSchema.load()

    def get_key_lesson(self):
        return  list(self.utils.read_from_json(LINKS_JSON_PATH).keys())

    def delete_lesson(self, key):
        self.utils.delete_link(key)

    @property
    def get_status_accept(self):
        return self.user.accept_terms_of_use

    @staticmethod
    async def on_start(e):
        await start()

    @staticmethod
    async def on_stop(e):
        await stop()