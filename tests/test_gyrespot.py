import pytest
from threading import Event
from pathlib import Path
from io import BytesIO
from gyjukebox.gyrespot import GYRespot
from gyjukebox.gyrespot.eventloop import EventLoop


def test_play_output(empty_app):
    with BytesIO() as f:
        end_of_track = Event()

        def on_music_delivery_callback(frames, num_frames):
            f.write(frames)
            f.flush()
            return num_frames

        def on_end_of_track():
            end_of_track.set()

        gyrespot = GYRespot(
            on_music_delivery_callback,
            on_end_of_track,
            username=empty_app.config["SPOTIFY_USERNAME"],
            password=empty_app.config["SPOTIFY_PASSWORD"],
        )

        eventloop = EventLoop(gyrespot)

        gyrespot.play("5VDaJPJ2AeqPImMYpsgFvp")

        eventloop.start()
        end_of_track.wait()
        eventloop.stop()

        assert len(f.getvalue()) == 50244600
