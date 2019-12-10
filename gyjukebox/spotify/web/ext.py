import collections
import logging
import spotify
import gi
from flask import current_app
from gyjukebox.spotify.pyspotify import create_logged_in_session
from gyjukebox.spotify.player import Player
from gyjukebox.spotify.player import NextTrackQueue
from gyjukebox.spotify.search import Client as SearchClient
from gyjukebox.spotify.streaming import SpotifyStreaming

gi.require_version("Gst", "1.0")
from gi.repository import GObject, Gst

_SpotifyExtConfig = collections.namedtuple(
    "SpotifyExtConfig", "session next_track_queue player search_client streaming loop"
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

        if spotify._session_instance is not None:
            logging.warn(
                "Cannot initialize spotify session twice in same process, reuse previous session"
            )
        session = spotify._session_instance or create_logged_in_session(
            app.config["SPOTIFY_USERNAME"], app.config["SPOTIFY_PASSWORD"]
        )
        next_track_queue = NextTrackQueue()
        player = Player(session, next_track_queue)
        search_client = SearchClient(
            app.config["SPOTIFY_CLIENT_ID"], app.config["SPOTIFY_CLIENT_SECRET"]
        )

        Gst.init([])

        streaming_options = {
            "location": app.config["SPOTIFY_HLS_LOCATION"],
            "playlist-location": app.config["SPOTIFY_HLS_PLAYLIST_LOCATION"],
            "playlist-root": app.config["SPOTIFY_HLS_PLAYLIST_ROOT"],
        }
        logging.info(streaming_options)
        streaming = SpotifyStreaming(session, streaming_options)
        loop = spotify.EventLoop(session)

        spotify_ext_config = _SpotifyExtConfig(
            session, next_track_queue, player, search_client, streaming, loop
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

    @property
    def search_client(self):
        return self.app.extensions["spotify_ext"].search_client

    @property
    def streaming(self):
        return self.app.extensions["spotify_ext"].streaming

    @property
    def loop(self):
        return self.app.extensions["spotify_ext"].loop
