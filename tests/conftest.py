import pytest
from flask import Flask
from gyjukebox.spotify.web import spotify_ext
from gyjukebox.login.web import login_ext
from gyjukebox.user.model import User
from gyjukebox.gyrespot.gyrespot import GYRespot
from gyjukebox.gstreamer import HLSStreaming
from gi.repository import Gst


@pytest.fixture()
def empty_app():
    app = Flask(__name__)
    app.config.from_object("config_test")
    with app.app_context():
        yield app


@pytest.fixture()
def spotify_session(empty_app):
    return spotify_ext.session


@pytest.fixture()
def login_token(empty_app):
    user = User("test_sub", "test_name")
    return login_ext.get_login_jwt_token(user)


@pytest.fixture()
def gyrespot(empty_app):
    return GYRespot(
        username=empty_app.config["SPOTIFY_USERNAME"],
        password=empty_app.config["SPOTIFY_PASSWORD"],
    )


@pytest.fixture()
def hlsstreaming(empty_app):
    Gst.init([])
    streaming_options = {
        "location": empty_app.config["SPOTIFY_HLS_LOCATION"],
        "playlist-location": empty_app.config["SPOTIFY_HLS_PLAYLIST_LOCATION"],
        "playlist-root": empty_app.config["SPOTIFY_HLS_PLAYLIST_ROOT"],
        "target-duration": empty_app.config["SPOTIFY_HLS_TARGET_DURATION"],
        "max-files": empty_app.config["SPOTIFY_HLS_MAX_FILES"],
        "playlist-length": empty_app.config["SPOTIFY_HLS_PLAYLIST_LENGTH"],
    }
    return HLSStreaming(streaming_options)
