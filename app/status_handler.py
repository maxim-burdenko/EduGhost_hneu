class StatusHandler:
    _observers = []

    def __init__(self):
        self._status = "неактивний"

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, status: str):
        self._status = status

        self.notify_observers(self._status)

    @classmethod
    def subscribe(cls, callback):
        cls._observers.append(callback)

    def notify_observers(self, status):
        for callback in self._observers:
            callback(status)
