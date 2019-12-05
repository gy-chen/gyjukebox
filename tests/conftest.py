import pytest
import configtest
from gyjukebox.spotify.pyspotify import create_logged_in_session


@pytest.fixture()
def spotify_session():
    return create_logged_in_session(configtest.SPOTIFY_USERNAME, configtest.SPOTIFY_PASSWORD)
