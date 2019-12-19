import collections
import logging
import spotify
import gi
from flask import current_app
from flask import _app_ctx_stack
from gyjukebox.spotify.pyspotify import create_logged_in_session
from gyjukebox.spotify.player import Player
from gyjukebox.spotify.search import Client as SearchClient
from gyjukebox.spotify.search import OAuthClient as OAuthSearchClient
from gyjukebox.spotify.streaming import SpotifyStreaming
from gyjukebox.spotify.next_track_queue import RoundRobinNextTrackQueue
from gyjukebox.spotify.next_track_queue import SimpleNextTrackQueue
from gyjukebox.oauth.web import oauth_ext
from gyjukebox.login.web import login_ext

gi.require_version("Gst", "1.0")
from gi.repository import GObject, Gst

logger = logging.getLogger(__name__)

_SpotifyExtConfig = collections.namedtuple(
    "SpotifyExtConfig", "session next_track_queue player streaming loop"
)


class SpotifyExt:
    def __init__(self, app=None):
        self._app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault("SPOTIFY_USERNAME", None)
        app.config.setdefault("SPOTIFY_PASSWORD", None)
        app.config.setdefault("SPOTIFY_CLIENT_ID", None)
        app.config.setdefault("SPOTIFY_CLIENT_SECRET", None)
        app.config.setdefault("SPOTIFY_HLS_LOCATION", None)
        app.config.setdefault("SPOTIFY_HLS_PLAYLIST_LOCATION", None)
        app.config.setdefault("SPOTIFY_HLS_PLAYLIST_ROOT", None)
        app.config.setdefault("SPOTIFY_HLS_PLAYLIST_LENGTH", 20)
        app.config.setdefault("SPOTIFY_HLS_TARGET_DURATION", 6)
        app.config.setdefault("SPOTIFY_HLS_MAX_FILES", 30)
        app.config.setdefault("SPOTIFY_QUEUE_TYPE", "RoundRobinNextTrackQueue")

        if spotify._session_instance is not None:
            logger.warning(
                "Cannot initialize spotify session twice in same process, reuse previous session"
            )
        session = spotify._session_instance or create_logged_in_session(
            app.config["SPOTIFY_USERNAME"], app.config["SPOTIFY_PASSWORD"]
        )
        if app.config["SPOTIFY_QUEUE_TYPE"] == "RoundRobinNextTrackQueue":
            logger.info("use RoundRobinNextTrackQueue")
            next_track_queue = RoundRobinNextTrackQueue()
        elif app.config["SPOTIFY_QUEUE_TYPE"] == "SimpleNextTrackQueue":
            logger.info("use SimpleNextTrackQueue")
            next_track_queue = SimpleNextTrackQueue()
        else:
            raise ValueError(f"Unsupport queue type {app.config['SPOTIFY_QUEUE_TYPE']}")
        player = Player(session, next_track_queue)

        Gst.init([])

        streaming_options = {
            "location": app.config["SPOTIFY_HLS_LOCATION"],
            "playlist-location": app.config["SPOTIFY_HLS_PLAYLIST_LOCATION"],
            "playlist-root": app.config["SPOTIFY_HLS_PLAYLIST_ROOT"],
            "target-duration": app.config["SPOTIFY_HLS_TARGET_DURATION"],
            "max-files": app.config["SPOTIFY_HLS_MAX_FILES"],
            "playlist-length": app.config["SPOTIFY_HLS_PLAYLIST_LENGTH"],
        }
        logger.debug(streaming_options)
        streaming = SpotifyStreaming(session, streaming_options)
        loop = spotify.EventLoop(session)

        spotify_ext_config = _SpotifyExtConfig(
            session, next_track_queue, player, streaming, loop
        )
        app.extensions["spotify_ext"] = spotify_ext_config

    @property
    def app(self):
        return self._app or current_app

    @property
    def session(self):
        return self.app.extensions["spotify_ext"].session

    @property
    def next_track_queue(self):
        return self.app.extensions["spotify_ext"].next_track_queue

    @property
    def player(self):
        return self.app.extensions["spotify_ext"].player

    def get_search_client(self, user):
        sub = user.sub
        if sub.startswith("spotify"):
            token_saver = oauth_ext.get_token_saver(user)
            return OAuthSearchClient(oauth_ext.spotify_provider, token_saver)
        return SearchClient(
            self.app.config["SPOTIFY_CLIENT_ID"],
            self.app.config["SPOTIFY_CLIENT_SECRET"],
        )

    @property
    def search_client(self):
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, "spotify_ext_search_client"):
                ctx.spotify_ext_search_client = self.get_search_client(
                    login_ext.current_user
                )
            return ctx.spotify_ext_search_client

    @property
    def streaming(self):
        return self.app.extensions["spotify_ext"].streaming

    @property
    def loop(self):
        return self.app.extensions["spotify_ext"].loop
