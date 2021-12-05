import os
from logging import Logger
from collections import namedtuple
from threading import Event, Lock
from queue import Queue, Empty
from pathlib import Path
from select import select
from subprocess import Popen, PIPE
from gyjukebox.gyrespot.eventemitter import EventEmitter

logger = Logger("GYRespot")


def connect_gyrespot_hls_streaming(gyrespot, hlsstreaming):
    gyrespot.on_music_delivery_callback = hlsstreaming.on_music_delivery
    gyrespot.on(GYRespot.EVENT_ON_END_OF_TRACK, hlsstreaming.on_end_of_track)


class TrackIsPlayingError(Exception):
    pass


class _ReadOutputTimeoutError(Exception):
    pass


class GYRespot(EventEmitter):
    EVENT_ON_END_OF_TRACK = "on_end_of_track"

    def __init__(
        self,
        username=None,
        password=None,
        executable=None,
    ):
        super().__init__()
        self._executable = (
            executable if executable is not None else self._find_gyrespot_executable()
        )
        self._on_music_delivery_callback = None
        self._start_lock = Lock()
        self._play_lock = Lock()
        self._is_started = Event()
        self._is_playing = Event()
        self._env = (
            {"USERNAME": username, "PASSWORD": password}
            if username is not None
            else None
        )
        self._p = None
        self._buffer = None
        self._q = Queue()
        self._wait_command = None

    @property
    def on_music_delivery_callback(self):
        return self._on_music_delivery_callback

    @on_music_delivery_callback.setter
    def on_music_delivery_callback(self, on_music_delivery_callback):
        self._on_music_delivery_callback = on_music_delivery_callback

    def process_events(self):
        assert self._on_music_delivery_callback is not None
        try:
            self._q.get(timeout=0.1)
        except Empty:
            pass

        with self._play_lock:
            consumed = False
            end_of_track = False
            try:
                buffer = self._read_stream()
                if len(buffer) != 0:
                    num_frames = len(buffer) // 4  # s16 2 ch -> 2 * 2 bytes
                    consumed = self._on_music_delivery_callback(buffer, num_frames)
                    if consumed:
                        self._clear_buffer()
            except _ReadOutputTimeoutError:
                pass

            try:
                if (
                    self._is_playing.is_set()
                    and not consumed
                    and (self._buffer is None or len(self._buffer) == 0)
                ):
                    # XXX: ignore command result for now
                    self._read_command_result()
                    self._is_playing.clear()
                    end_of_track = True
            except _ReadOutputTimeoutError:
                pass

        # prevent deadlock
        if end_of_track:
            self.emit(self.EVENT_ON_END_OF_TRACK)

    def play(self, track_id):
        self._start()
        with self._play_lock:
            if self._is_playing.is_set():
                raise TrackIsPlayingError()
            self._write_command(f"play {track_id}")
            self._is_playing.set()

    def _start(self):
        if not self._is_started.is_set():
            with self._start_lock:
                if not self._is_started.is_set():
                    self._real_start()
                    self._is_started.set()

    def _real_start(self):
        self._p = Popen(
            [self._executable],
            env=self._env,
            stdout=PIPE,
            stdin=PIPE,
            stderr=PIPE,
            bufsize=0,
        )

    def _write_command(self, command):
        logger.info(f"send command: {command}")
        self._p.stdin.write(f"{command}\n".encode())
        self._p.stdin.flush()

    def _read_command_result(self):
        try:
            (pstderr,), _, _ = select([self._p.stderr], [], [], 0.01)
            return self._parse_command_result(pstderr.readline())
        except (ValueError, AttributeError):
            raise _ReadOutputTimeoutError()

    def _parse_command_result(self, raw):
        # XXX: only play command here and no need to check play result, ignore parsing for now
        logger.info(f"command result: {raw}")
        return None

    def _read_stream(self):
        if self._buffer is not None:
            return self._buffer

        try:
            (pstdout,), _, _ = select([self._p.stdout], [], [], 0.01)
            self._buffer = pstdout.read(32768)
            return self._buffer
        except (ValueError, AttributeError):
            raise _ReadOutputTimeoutError()

    def _clear_buffer(self):
        self._buffer = None

    def _find_gyrespot_executable(self):
        return str((Path(__file__).parent / "gyrespot").absolute())
