def connect_gyrespot_hls_streaming(gyrespot, hlsstreaming):
    gyrespot.on_music_delivery_callback = hlsstreaming.on_music_delivery
