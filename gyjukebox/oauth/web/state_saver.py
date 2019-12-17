from flask import session
from gyjukebox.oauth.state_saver import BaseStateSaver


class SessionStateSaver(BaseStateSaver):
    _STATE_KEY = "OAUTH_STATE"

    def save(self, state):
        session[self._STATE_KEY] = state

    def get(self):
        return session[self._STATE_KEY]
