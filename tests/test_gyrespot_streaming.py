from threading import Event
from gyjukebox.gyrespot import GYRespot, connect_gyrespot_hls_streaming
from gyjukebox.gyrespot.eventloop import EventLoop


def test_streaming(gyrespot, hlsstreaming):
    end_of_track = Event()

    def on_end_of_track():
        print("here")
        end_of_track.set()

    eventloop = EventLoop(gyrespot)
    connect_gyrespot_hls_streaming(gyrespot, hlsstreaming)
    gyrespot.on(GYRespot.EVENT_ON_END_OF_TRACK, on_end_of_track)

    hlsstreaming.start()
    eventloop.start()

    gyrespot.play("spotify:track:1WmgfRc0438mZ0ojv5LDrS")
    end_of_track.wait()

    end_of_track.clear()
    gyrespot.play("spotify:track:7vPWfW9tpx38Jb7MwUfmmX")
    end_of_track.wait()

    end_of_track.clear()
    gyrespot.play("spotify:track:3QFhZ0lCZRcT9zLRQHmMdu")
    end_of_track.wait()

    end_of_track.clear()
    gyrespot.play("spotify:track:6W7dOcsg7jSGRdJ7T4B0A6")
    end_of_track.wait()

    end_of_track.clear()
    gyrespot.play("spotify:track:5VDaJPJ2AeqPImMYpsgFvp")
    end_of_track.wait()

    eventloop.stop()
