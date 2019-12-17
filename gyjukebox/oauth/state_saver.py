class BaseStateSaver:
    def save(self, state):
        return NotImplemented

    def get(self):
        return NotImplemented
