import base64
import json
from requests_oauthlib import OAuth2Session


class BaseOAuthProvider:
    """Base implementations of OAuthProvider

    Available options:
        client_id
        client_secret
        authorization_url
        token_url
        refresh_url
        user_url
        redirect_uri
        scope

    Args:
        state_saver (gyjukebox.oauth.state_saver.BaseStateSaver)
        token_saver (gyjukebox.oauth.token_saver.BaseTokenSaver)
        options (dict)
    """

    def __init__(self, state_saver, options={}):
        self._state_saver = state_saver
        self._client_id = options.get("client_id")
        self._client_secret = options.get("client_secret")
        self._authorization_url = options.get("authorization_url")
        self._token_url = options.get("token_url")
        self._refresh_url = options.get("refresh_url")
        self._user_url = options.get("user_url")
        self._redirect_uri = options.get("redirect_uri")
        self._scope = options.get("scope")

    def get_authorization_url(self):
        sess = OAuth2Session(
            self._client_id, redirect_uri=self._redirect_uri, scope=self._scope
        )
        authorization_url, state = sess.authorization_url(self._authorization_url)
        self._state_saver.save(state)
        return authorization_url

    def fetch_token(self, response_url):
        sess = OAuth2Session(
            self._client_id,
            redirect_uri=self._redirect_uri,
            state=self._state_saver.get(),
        )
        return sess.fetch_token(
            self._token_url,
            client_secret=self._client_secret,
            authorization_response=response_url,
        )

    def refresh_token(self, token):
        return NotImplemented

    def fetch_user(self, token):
        return NotImplemented


class GoogleOAuthProvider(BaseOAuthProvider):
    def __init__(self, state_saver, options={}):
        options_ = {
            "authorization_url": "https://accounts.google.com/o/oauth2/v2/auth",
            "token_url": "https://oauth2.googleapis.com/token",
            "scope": "profile",
        }
        options_.update(options)
        super().__init__(state_saver, options_)

    def fetch_user(self, token):
        return self._decode_user_from_id_token(token["id_token"])

    def _decode_user_from_id_token(self, id_token):
        _, payload_raw, _ = id_token.split(".")
        missing_padding = 4 - (len(payload_raw) % 4)
        payload_raw_decoded = base64.urlsafe_b64decode(
            payload_raw + "=" * missing_padding
        )
        payload = json.loads(payload_raw_decoded)
        return payload


class SpotifyOAuthProvider(BaseOAuthProvider):
    def __init__(self, state_saver, options={}):
        options_ = {
            "authorization_url": "https://accounts.spotify.com/authorize",
            "token_url": "https://accounts.spotify.com/api/token",
            "refresh_url": "https://accounts.spotify.com/api/token",
            "scope": "user-read-email user-top-read playlist-read-private user-follow-read user-library-read",
        }
        options_.update(options)
        super().__init__(state_saver, options_)

    def refresh_token(self, token):
        sess = OAuth2Session(self._client_id, token=token)
        return sess.refresh_token(
            self._refresh_url,
            client_id=self._client_id,
            client_secret=self._client_secret
        )

    def fetch_user(self, token):
        sess = OAuth2Session(self._client_id, token=token)
        return sess.get("https://api.spotify.com/v1/me").json()
