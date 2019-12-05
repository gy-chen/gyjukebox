import queue
import time
import spotify
from spotify.player import PlayerState
from spotify.utils import EventEmitter


class NextTrackQueue:
    def __init__(self):
        self._queue = queue.Queue()

    def add_track(self, request_track):
        """Add track to the queue

        Args:
            request_track: gyjukebox.spotify.model.RequestTrack
        """
        self._queue.put(request_track)

    def next_track(self):
        """Get next track to play

        Returns:
            gyjukebox.spotify.model.RequestTrack
        """
        try:
            return self._queue.get(False)
        except queue.Empty:
            raise _NoNextTrackError()

    def size(self):
        return self._queue.qsize()


class Player(EventEmitter):
    """Spotify player

    Args:
        session (spotify.Session)
        queue (gyjukebox.spotify.player.NextTrackQueue)
    """

    def __init__(self, session, queue):
        super().__init__()
        self._session = session
        self._queue = queue
        self._playing_track = None
        self._track_start_timestamp = None

        session.on(spotify.SessionEvent.END_OF_TRACK, self._on_end_of_track)

    def play(self):
        """Start the player

        if player is paused, resume playing, otherwise load and play next track.
        """
        if self._session.player.state == PlayerState.PLAYING:
            return
        if self._session.player.state != PlayerState.PAUSED:
            try:
                self._playing_track = self._load_next_track()
            except _NoNextTrackError:
                return
            self._track_start_timestamp = time.time()
            self.emit('next_track', self._playing_track, self._track_start_timestamp)
        self._session.player.play()

    def _load_next_track(self):
        request_track = self._queue.next_track()
        resource = self._session.get_track(request_track.track.uri).load()
        self._session.player.load(resource)
        return request_track

    def get_playing_track(self):
        return self._playing_track

    def get_track_start_timestamp(self):
        return self._track_start_timestamp

    def _on_end_of_track(self, _):
        self.emit('end_of_track', self._playing_track)
        self._track_start_timestamp = None
        try:
            self._playing_track = self._load_next_track()
        except _NoNextTrackError:
            return
        self._track_start_timestamp = time.time()
        self.emit('next_track', self._playing_track, self._track_start_timestamp)
        self.play()

    def on_end_of_track(self, callback, *user_args):
        self.on('end_of_track', callback, *user_args)

    def on_next_track(self, callback, *user_args):
        self.on('next_track', callback, *user_args)

class _NoNextTrackError(Exception):
    pass