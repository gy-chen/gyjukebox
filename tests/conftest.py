import pytest
from flask import Flask
from gyjukebox.spotify.web import spotify_ext
from gyjukebox.login.web import login_ext
from gyjukebox.user.model import User


@pytest.fixture()
def empty_app():
    app = Flask(__name__)
    app.config.from_object('config_test')
    with app.app_context():
        yield app


@pytest.fixture()
def spotify_session(empty_app):
    return spotify_ext.session


@pytest.fixture()
def login_token(empty_app):
    user = User("test_sub", "test_name")
    return login_ext.get_login_jwt_token(user)
