from timezonefinder import TimezoneFinder

tf = TimezoneFinder()

def get_timezone(lat, lon):

    timezone = tf.timezone_at(
        lat=float(lat),
        lng=float(lon)
    )

    return timezone