class BaseTokenSaver:
    """Defined shared implemenations and apis for TokenSaver

    """

    def save(self, token):
        """Save OAuth token

        Args:
            token (dict): dict usually contain fields access_token, token_type, expires_in, refresh_token
        """
        return NotImplemented

    def get(self):
        "Get saved token"
        return NotImplemented


class NoSaveTokenSaver(BaseTokenSaver):
    """TokenSaver that not save token

    Use this if no need to save token (e.g. no need to access other api after obtained access token)
    """

    def save(self, token):
        pass

    def get(self):
        return None


class InMemoryTokenSaver(BaseTokenSaver):
    """Just store token in memory

    Args:
        sub: key for store and retrive token
    """

    _STORAGE = {}

    def __init__(self, sub):
        self._sub = sub

    def save(self, token):
        self._STORAGE[self._sub] = token

    def get(self):
        return self._STORAGE.get(self._sub)
