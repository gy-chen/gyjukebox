import collections

Track = collections.namedtuple("Track", "uri name duration_ms")
RequestTrack = collections.namedtuple("RequestTrack", "track user")

