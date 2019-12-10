import collections

Track = collections.namedtuple("Track", "uri name artists duration_ms")
RequestTrack = collections.namedtuple("RequestTrack", "track user")

