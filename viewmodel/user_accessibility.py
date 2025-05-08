from app.status_handler import StatusHandler

class UserAccessibility:
    def __init__(self, model: StatusHandler):
        self.model = model
        self.status = self.model.status
        self._view_update_callback = None
        self.model.subscribe(self._model_changed)

    def _model_changed(self, new_status: str):
        self.status = new_status
        if self._view_update_callback:
            self._view_update_callback(new_status)

    def bind_to_view(self, callback):
        self._view_update_callback = callback

    def change_status(self):
        new_status = "активний" if self.status != "активний" else "неактивний"
        self.model.status = new_status
