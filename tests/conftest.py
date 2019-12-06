import pytest
import configtest
from flask import Flask
from gyjukebox.spotify.pyspotify import create_logged_in_session


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
        return app
