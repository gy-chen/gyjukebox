import pytest
import configtest
from gyjukebox.spotify.search import Client


@pytest.fixture()
def client():
    return Client(configtest.SPOTIFY_CLIENT_ID, configtest.SPOTIFY_CLIENT_SECRET)


def test_search_without_error(client):
    client.search("Hello World")
