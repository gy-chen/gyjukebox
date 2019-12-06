import pytest
import configtest
from gyjukebox.spotify.search import Client


@pytest.fixture()
def client():
    return Client(configtest.SPOTIFY_CLIENT_ID, configtest.SPOTIFY_CLIENT_SECRET)


def test_search_without_error(client):
    client.search("Hello World")

def test_get_track_without_error(client):
    client.get_track("spotify:track:6xZtSE6xaBxmRozKA0F6TA")
    r = client.get_track("6xZtSE6xaBxmRozKA0F6TA")
    
    pytest.raises(ValueError, lambda: client.get_track("track:6xZtSE6xaBxmRozKA0F6TA"))