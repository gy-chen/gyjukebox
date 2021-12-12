import logging
from threading import Lock
from gyjukebox.gyrespot.gyrespot import GYRespot
from gyjukebox.spotify.next_track_queue import NoNextTrackError

logger = logging.getLogger(__name__)


class Player:
    def __init__(self, gyrespot, next_track_queue):
        self._gyrespot = gyrespot
        self._next_track_queue = next_track_queue
        self._change_song_lock = Lock()

        self._current_track = None
        self._gyrespot.on(GYRespot.EVENT_ON_END_OF_TRACK, self._on_end_of_track)

    def play(self):
        logger.info("Try to start player")
        with self._change_song_lock:
            if self._current_track is not None:
                logger.info("A track is playing, do nothing")
                return
            try:
                logger.info("Try to play next track")
                next_track = self._get_next_track()
                logger.info(f"Got next track {next_track}")
                self._gyrespot.play(next_track.track.uri)
                self._current_track = next_track
            except NoNextTrackError:
                logger.info("No next track to paly")

    def get_playing_track(self):
        return self._current_track

    def _get_next_track(self):
        return self._next_track_queue.next_track()

    def _on_end_of_track(self):
        with self._change_song_lock:
            self._current_track = None
        self.play()
