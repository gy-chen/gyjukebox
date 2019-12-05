import threading
import spotify
from gyjukebox.spotify.player import NextTrackQueue
from gyjukebox.spotify.player import Player
from gyjukebox.spotify.model import Track
from gyjukebox.spotify.model import RequestTrack
from gyjukebox.user.model import User


def test_player(spotify_session):
    empty = threading.Event()
    next_track = threading.Event()
    q = NextTrackQueue()
    player = Player(spotify_session, q)
    audio = spotify.AlsaSink(spotify_session)
    loop = spotify.EventLoop(spotify_session)

    t = Track("spotify:track:6xZtSE6xaBxmRozKA0F6TA", "DEMO TRACK", 10)
    u = User("test_sub", "test_user")
    r = RequestTrack(t, u)
    q.add_track(r)
    q.add_track(r)

    def on_end_of_track(track):
        if q.size() == 0:
            empty.set()

    def on_next_track(track, timestamp):
        next_track.set()

    player.on_end_of_track(on_end_of_track)
    player.on_next_track(on_next_track)

    loop.start()
    player.play()

    empty.wait()
    next_track.wait()
