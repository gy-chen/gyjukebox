import pytest
import configtest
from flask import Flask
from gyjukebox.spotify.pyspotify import create_logged_in_session
from gyjukebox.login.web import login_ext
from gyjukebox.user.model import User


@pytest.fixture()
def spotify_session():
    return create_logged_in_session(
        configtest.SPOTIFY_USERNAME, configtest.SPOTIFY_PASSWORD
    )


@pytest.fixture()
def empty_app():
    app = Flask(__name__)
    app.config.from_object(configtest)
    with app.app_context():
        yield app


@pytest.fixture()
def login_token(empty_app):
    user = User("test_sub", "test_name")
    return login_ext.get_login_jwt_token(user)
