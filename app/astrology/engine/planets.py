import swisseph as swe
PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
    "Rahu": swe.MEAN_NODE,  # Use mean node for Rahu
   
}

def calculate_ketu(rahu_longitude):
    return (rahu_longitude + 180.0) % 360.0


