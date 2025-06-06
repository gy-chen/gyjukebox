import queue
import time
import logging
import threading
import spotify
from spotify.player import PlayerState
from spotify.utils import EventEmitter
from gyjukebox.spotify.next_track_queue import NoNextTrackError

logger = logging.getLogger(__name__)


class Player(EventEmitter):
    """Spotify player

    Args:
        session (spotify.Session)
        queue (gyjukebox.spotify.next_track_queue.NextTrackQueue)
    """

    def __init__(self, session, queue):
        super().__init__()
        self._session = session
        self._queue = queue
        self._playing_track = None
        self._track_start_timestamp = None
        self._changing_song_lock = threading.Lock()

        session.on(spotify.SessionEvent.END_OF_TRACK, self._on_end_of_track)

    def play(self):
        """Start the player

        if player is paused, resume playing, otherwise load and play next track.
        """
        logger.info("Try to start player")
        if self._session.player.state == PlayerState.PLAYING:
            logger.info("Player is in PLAYING state, do nothing.")
            return
        if self._session.player.state != PlayerState.PAUSED:
            if not self._changing_song_lock.acquire(blocking=False):
                logger.info("cannot acquire changing song lock, do nothing")
                return
            try:
                try:
                    self._playing_track = self._load_next_track()
                    logger.info("Got next track %s", self._playing_track)
                except NoNextTrackError:
                    self._track_start_timestamp = None
                    self._playing_track = None
                    return
                self._track_start_timestamp = time.time()
                self.emit(
                    "next_track", self._playing_track, self._track_start_timestamp
                )
                self._session.player.play()
            finally:
                self._changing_song_lock.release()
        else:
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
        self.emit("end_of_track", self._playing_track)
        logger.debug("End of track")
        logger.debug("Current player state: %s", self._session.player.state)
        if not self._changing_song_lock.acquire(blocking=False):
            logger.debug("cannot acquire changing song lock, do nothing")
            return
        try:
            self._track_start_timestamp = None
            try:
                self._playing_track = self._load_next_track()
                logger.info("Got next track %s", self._playing_track)
            except NoNextTrackError:
                self._track_start_timestamp = None
                self._playing_track = None
                return
            self._track_start_timestamp = time.time()
            self.emit("next_track", self._playing_track, self._track_start_timestamp)
            self._session.player.play()
        finally:
            self._changing_song_lock.release()

    def on_end_of_track(self, callback, *user_args):
        self.on("end_of_track", callback, *user_args)

    def on_next_track(self, callback, *user_args):
        self.on("next_track", callback, *user_args)
