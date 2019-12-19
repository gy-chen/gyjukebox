import pytest
import logging
import config_test
from gyjukebox.spotify.search import Client
from gyjukebox.spotify.search import OAuthClient
from gyjukebox.oauth.token_saver import InMemoryTokenSaver
from gyjukebox.oauth.provider import SpotifyOAuthProvider
from gyjukebox.oauth.state_saver import BaseStateSaver


@pytest.fixture(scope="module")
def client():
    return Client(config_test.SPOTIFY_CLIENT_ID, config_test.SPOTIFY_CLIENT_SECRET)


@pytest.fixture(scope="module")
def oauth_client():
    token = config_test.OAUTH_SPOTIFY_TEST_TOKEN
    token_saver = InMemoryTokenSaver("test")
    token_saver.save(token)

    state_saver = BaseStateSaver()
    options = {
        "client_id": config_test.OAUTH_SPOTIFY_CLIENT_ID,
        "client_secret": config_test.OAUTH_SPOTIFY_CLIENT_SECRET,
    }
    provider = SpotifyOAuthProvider(state_saver, options)

    client = OAuthClient(provider, token_saver)
    return client


def test_search_without_error(client, oauth_client):
    client.search("Hello World")
    oauth_client.search("Hello World")


def test_get_track_without_error(client, oauth_client):
    client.get_track("spotify:track:6xZtSE6xaBxmRozKA0F6TA")
    client.get_track("6xZtSE6xaBxmRozKA0F6TA")
    pytest.raises(ValueError, lambda: client.get_track("track:6xZtSE6xaBxmRozKA0F6TA"))

    oauth_client.get_track("spotify:track:6xZtSE6xaBxmRozKA0F6TA")
    oauth_client.get_track("6xZtSE6xaBxmRozKA0F6TA")
    pytest.raises(
        ValueError, lambda: oauth_client.get_track("track:6xZtSE6xaBxmRozKA0F6TA")
    )


def test_get_album_tracks_without_error(client, oauth_client):
    client.get_album_tracks("spotify:album:7jyiXKzJYgJ24IqlGMKcjN")
    oauth_client.get_album_tracks("spotify:album:7jyiXKzJYgJ24IqlGMKcjN")


def test_get_artist_albums_without_error(client, oauth_client):
    client.get_artist_albums("spotify:artist:4pJgbKhO6gZUZDXLQ8deHp")
    oauth_client.get_artist_albums("spotify:artist:4pJgbKhO6gZUZDXLQ8deHp")


def test_get_artist_top_tracks_without_error(client, oauth_client):
    client.get_artist_albums("spotify:artist:4pJgbKhO6gZUZDXLQ8deHp")
    oauth_client.get_artist_albums("spotify:artist:4pJgbKhO6gZUZDXLQ8deHp")


def test_get_playlist_tracks_without_error(client, oauth_client):
    client.get_playlist_tracks("spotify:playlist:5TkjKcp6CCUsFVxfgzJGqR")
    oauth_client.get_playlist_tracks("spotify:playlist:5TkjKcp6CCUsFVxfgzJGqR")


def test_get_user_top_artists(client, oauth_client):
    assert client.get_user_top_artists() is None
    oauth_client.get_user_top_artists()


def test_get_user_top_tracks(client, oauth_client):
    assert client.get_user_top_tracks() is None
    oauth_client.get_user_top_tracks()


def test_get_user_playlists(client, oauth_client):
    assert client.get_user_playlists() is None
    oauth_client.get_user_playlists()


def test_get_user_albums(client, oauth_client):
    assert client.get_user_albums() is None
    oauth_client.get_user_albums()


def test_get_user_tracks(client, oauth_client):
    assert client.get_user_tracks() is None
    oauth_client.get_user_tracks()
