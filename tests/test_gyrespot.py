from threading import Event
from io import BytesIO
from gyjukebox.gyrespot import GYRespot
from gyjukebox.gyrespot.eventloop import EventLoop


def test_play_output(gyrespot):
    with BytesIO() as f:
        end_of_track = Event()

        def on_music_delivery_callback(frames, num_frames):
            f.write(frames)
            f.flush()
            return num_frames

        def on_end_of_track():
            end_of_track.set()

        gyrespot.on_music_delivery_callback = on_music_delivery_callback
        gyrespot.on(GYRespot.EVENT_ON_END_OF_TRACK, on_end_of_track)

        eventloop = EventLoop(gyrespot)

        gyrespot.play("5VDaJPJ2AeqPImMYpsgFvp")

        eventloop.start()
        end_of_track.wait()
        eventloop.stop()

        assert len(f.getvalue()) == 50244600
