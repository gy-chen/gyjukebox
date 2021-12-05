import logging
import gi
from flask import _app_ctx_stack, current_app
from gyjukebox.spotify.search import Client as SearchClient
from gyjukebox.spotify.search import OAuthClient as OAuthSearchClient
from gyjukebox.spotify.next_track_queue import RoundRobinNextTrackQueue
from gyjukebox.spotify.next_track_queue import SimpleNextTrackQueue
from gyjukebox.oauth.web import oauth_ext
from gyjukebox.login.web import login_ext

gi.require_version("Gst", "1.0")
from gi.repository import GObject, Gst

logger = logging.getLogger(__name__)


class SpotifyExt:
    def __init__(self, app=None):
        self._app = app
        if app is not None:
            self.init_app(app)

    def _init_pyspotify_backend(self, app, next_track_queue, hls_options):
        import spotify
        from gyjukebox.spotify.pyspotify import create_logged_in_session
        from gyjukebox.spotify.player import Player
        from gyjukebox.spotify.streaming import SpotifyStreaming

        if spotify._session_instance is not None:
            logger.warning(
                "Cannot initialize spotify session twice in same process, reuse previous session"
            )
        session = spotify._session_instance or create_logged_in_session(
            app.config["SPOTIFY_USERNAME"], app.config["SPOTIFY_PASSWORD"]
        )
        player = Player(session, next_track_queue)
        streaming = SpotifyStreaming(session, hls_options)
        loop = spotify.EventLoop(session)
        return (session, streaming, player, loop)

    def _init_gyrespot_backend(self, app, next_track_queue, hls_options):
        from gyjukebox.gyrespot import GYRespot, connect_gyrespot_hls_streaming
        from gyjukebox.gyrespot.player import Player
        from gyjukebox.gyrespot.eventloop import EventLoop
        from gyjukebox.gstreamer import HLSStreaming

        gyrespot = GYRespot(
            app.config["SPOTIFY_USERNAME"], app.config["SPOTIFY_PASSWORD"]
        )

        streaming = HLSStreaming(hls_options)
        player = Player(gyrespot, next_track_queue)
        loop = EventLoop(gyrespot)

        connect_gyrespot_hls_streaming(gyrespot, streaming)

        return (gyrespot, streaming, player, loop)

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
        app.config.setdefault("SPOTIFY_BACKEND_TYPE", "GYRESPOT")  # GYRESPOT, PYSPOTIFY

        if app.config["SPOTIFY_QUEUE_TYPE"] == "RoundRobinNextTrackQueue":
            logger.info("use RoundRobinNextTrackQueue")
            next_track_queue = RoundRobinNextTrackQueue()
        elif app.config["SPOTIFY_QUEUE_TYPE"] == "SimpleNextTrackQueue":
            logger.info("use SimpleNextTrackQueue")
            next_track_queue = SimpleNextTrackQueue()
        else:
            raise ValueError(f"Unsupport queue type {app.config['SPOTIFY_QUEUE_TYPE']}")

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

        if app.config["SPOTIFY_BACKEND_TYPE"] == "PYSPOTIFY":
            session, streaming, player, loop = self._init_pyspotify_backend(
                app, next_track_queue, streaming_options
            )
            self._next_track_queue = next_track_queue
            self._streaming = streaming
            self._player = player
            self._loop = loop
        elif app.config["SPOTIFY_BACKEND_TYPE"] == "GYRESPOT":
            gyrespot, streaming, player, loop = self._init_gyrespot_backend(
                app, next_track_queue, streaming_options
            )

            print("here")
            self._next_track_queue = next_track_queue
            self._gyrespot = gyrespot
            self._streaming = streaming
            self._player = player
            self._loop = loop

        app.extensions["spotify_ext"] = self

    @property
    def next_track_queue(self):
        return self._next_track_queue

    @property
    def player(self):
        return self._player

    def get_search_client(self, user):
        sub = user.sub
        if sub.startswith("spotify"):
            token_saver = oauth_ext.get_token_saver(user)
            return OAuthSearchClient(oauth_ext.spotify_provider, token_saver)
        return SearchClient(
            current_app.config["SPOTIFY_CLIENT_ID"],
            current_app.config["SPOTIFY_CLIENT_SECRET"],
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
        return self._streaming

    @property
    def loop(self):
        return self._loop
