from threading import Thread


class EventLoop(Thread):
    def __init__(self, session):
        super().__init__()
        self._session = session
        self._runnable = True

    def start(self):
        Thread.start(self)

    def stop(self):
        self._runnable = False

    def run(self):
        while self._runnable:
            self._session.process_events()