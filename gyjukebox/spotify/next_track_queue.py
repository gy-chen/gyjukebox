"""Provide next track queues of different strategy"""
import bisect
import logging
import queue
import threading

logger = logging.getLogger(__name__)


class BaseNextTrackQueue:
    def add_track(self, request):
        """Add track to the queue

        Args:
            request_track: gyjukebox.spotify.model.RequestTrack
        """
        return NotImplemented

    def next_track(self):
        """Get next track to play

        Returns:
            gyjukebox.spotify.model.RequestTrack
        """
        return NotImplemented

    def size(self):
        """Size of queued songs

        Returns:
            int
        """
        return NotImplemented


class SimpleNextTrackQueue(BaseNextTrackQueue):
    def __init__(self):
        self._queue = queue.Queue()

    def add_track(self, request_track):
        logger.info("Add track %s", request_track)
        self._queue.put(request_track)

    def next_track(self):
        try:
            logger.debug("Try to load next track")
            return self._queue.get(False)
        except queue.Empty:
            logger.debug("No next track")
            raise NoNextTrackError()

    def size(self):
        return self._queue.qsize()


class RoundRobinNextTrackQueue(BaseNextTrackQueue):
    def __init__(self):
        # expect item is (user, song1, song2, ...)
        self._q = []
        self._current_index = 0
        self._q_lock = threading.Lock()

    def add_track(self, request_track):
        logger.info("Add track %s", request_track)
        with self._q_lock:
            i = bisect.bisect_left(self._q, (request_track.user,))
            if i != len(self._q) and self._q[i][0] == request_track.user:
                item = self._q[i]
            else:
                item = (request_track.user,)
                self._q.insert(i, item)
            item += (request_track,)
            self._q[i] = item

    def next_track(self):
        logger.debug("Try to load next track")
        with self._q_lock:
            if not self._q:
                raise NoNextTrackError()
            for item in self._q[self._current_index :] + self._q[: self._current_index]:
                if len(item) == 1:
                    logger.debug(
                        "All tracks requested by user %s has played, continue to next one",
                        item[0],
                    )
                    self._current_index += 1
                    self._current_index %= len(self._q)
                    continue
                self._q[self._current_index] = (item[0],) + item[2:]
                self._current_index += 1
                self._current_index %= len(self._q)
                return item[1]
            logger.debug("No next track")
            raise NoNextTrackError()

    def size(self):
        return sum(map(len, self._q)) - len(self._q)


class NoNextTrackError(Exception):
    pass
