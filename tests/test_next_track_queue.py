import pytest
from gyjukebox.user.model import User
from gyjukebox.spotify.model import RequestTrack, Track
from gyjukebox.spotify.next_track_queue import RoundRobinNextTrackQueue
from gyjukebox.spotify.next_track_queue import NoNextTrackError


def _make_test_track(i):
    return Track(f"track{i}_uri", f"track{i}_name", ("track{i}_artist1",), 0)


def test_one_user_round_robin_next_track_queue():
    user1 = User("user1_sub", "user1_name")
    track1 = RequestTrack(_make_test_track(1), user1)
    track2 = RequestTrack(_make_test_track(2), user1)
    track3 = RequestTrack(_make_test_track(3), user1)

    q = RoundRobinNextTrackQueue()
    q.add_track(track1)
    q.add_track(track2)
    q.add_track(track3)

    assert q.size() == 3
    assert q.next_track() == track1
    assert q.next_track() == track2
    assert q.next_track() == track3
    assert pytest.raises(NoNextTrackError, q.next_track)

def test_two_user_round_robin_next_track_queue():
    user1 = User("user1_sub", "user1_name")
    user2 = User("user2_sub", "user2_name")
    track1 = RequestTrack(_make_test_track(1), user1)
    track2 = RequestTrack(_make_test_track(2), user2)
    track3 = RequestTrack(_make_test_track(3), user1)
    track4 = RequestTrack(_make_test_track(4), user2)
    track5 = RequestTrack(_make_test_track(5), user1)
    track6 = RequestTrack(_make_test_track(6), user2)

    q = RoundRobinNextTrackQueue()
    q.add_track(track1)
    q.add_track(track2)
    q.add_track(track3)
    q.add_track(track4)
    q.add_track(track5)
    q.add_track(track6)

    assert q.size() == 6
    assert q.next_track() == track1
    assert q.next_track() == track2
    assert q.next_track() == track3
    assert q.next_track() == track4
    assert q.next_track() == track5
    assert q.next_track() == track6
    assert pytest.raises(NoNextTrackError, q.next_track)


