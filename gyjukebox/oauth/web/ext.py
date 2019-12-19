import base64
import collections
import json
from flask import current_app, session, request
from requests_oauthlib import OAuth2Session
from gyjukebox.oauth.web.state_saver import SessionStateSaver
from gyjukebox.oauth.provider import GoogleOAuthProvider
from gyjukebox.oauth.provider import SpotifyOAuthProvider
from gyjukebox.oauth.token_saver import NoSaveTokenSaver
from gyjukebox.oauth.token_saver import InMemoryTokenSaver

_OAuthConfig = collections.namedtuple("OAuthConfig", "google_provider spotify_provider")


class OAuth:
    def __init__(self, app=None):
        self._app = app

    @property
    def app(self):
        if self._app:
            return self._app
        return current_app

    def init_app(self, app):
        app.config.setdefault("OAUTH_GOOGLE_CLIENT_ID", None)
        app.config.setdefault("OAUTH_GOOGLE_CLIENT_SECRET", None)
        app.config.setdefault("OAUTH_GOOGLE_REDIRECT_URI", None)

        app.config.setdefault("OAUTH_SPOTIFY_CLIENT_ID", None)
        app.config.setdefault("OAUTH_SPOTIFY_CLIENT_SECRET", None)
        app.config.setdefault("OAUTH_SPOTIFY_REDIRECT_URI", None)

        state_saver = SessionStateSaver()

        google_oauth_options = {}
        if app.config.get("OAUTH_GOOGLE_CLIENT_ID"):
            google_oauth_options["client_id"] = app.config["OAUTH_GOOGLE_CLIENT_ID"]
        if app.config.get("OAUTH_GOOGLE_CLIENT_SECRET"):
            google_oauth_options["client_secret"] = app.config[
                "OAUTH_GOOGLE_CLIENT_SECRET"
            ]
        if app.config.get("OAUTH_GOOGLE_REDIRECT_URI"):
            google_oauth_options["redirect_uri"] = app.config[
                "OAUTH_GOOGLE_REDIRECT_URI"
            ]
        google_oauth_provider = GoogleOAuthProvider(state_saver, google_oauth_options)

        spotify_oauth_options = {}
        if app.config.get("OAUTH_SPOTIFY_CLIENT_ID"):
            spotify_oauth_options["client_id"] = app.config["OAUTH_SPOTIFY_CLIENT_ID"]
        if app.config.get("OAUTH_SPOTIFY_CLIENT_SECRET"):
            spotify_oauth_options["client_secret"] = app.config[
                "OAUTH_SPOTIFY_CLIENT_SECRET"
            ]
        if app.config.get("OAUTH_SPOTIFY_REDIRECT_URI"):
            spotify_oauth_options["redirect_uri"] = app.config[
                "OAUTH_SPOTIFY_REDIRECT_URI"
            ]
        spotify_oauth_provider = SpotifyOAuthProvider(
            state_saver, spotify_oauth_options
        )

        oauth_config = _OAuthConfig(google_oauth_provider, spotify_oauth_provider)
        app.extensions["oauth_ext"] = oauth_config

    @property
    def google_provider(self):
        return self.app.extensions["oauth_ext"].google_provider

    @property
    def spotify_provider(self):
        return self.app.extensions["oauth_ext"].spotify_provider

    def get_token_saver(self, user):
        """Get token saver

        Args:
            user (gyjukebox.user.model.User)
        """
        sub = user.sub
        if sub.startswith("spotify"):
            return InMemoryTokenSaver(sub)
        return NoSaveTokenSaver()
