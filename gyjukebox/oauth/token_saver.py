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
