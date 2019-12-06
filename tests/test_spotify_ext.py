from gyjukebox.spotify.web.ext import SpotifyExt


def test_spotiy_ext(empty_app):
    spotify = SpotifyExt(empty_app)
    assert spotify.session is not None
    assert spotify.next_track_queue is not None
    assert spotify.player is not None
    assert spotify.search_client is not None
