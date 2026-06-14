from app.astrology.ephemeris.swiss import SwissEphemeris
from app.astrology.engine.planets import PLANETS

jd = SwissEphemeris.calculate_julian_day(
    1987,
    4,
    29,
    12.5
)

print("Julian Day:", jd)

ayanamsa = SwissEphemeris.get_lahiri_ayanamsa(jd)

print("Lahiri Ayanamsa:", ayanamsa)

for planet_name, planet_id in PLANETS.items():

    longitude = SwissEphemeris.get_planet_longitude(
        jd,
        planet_id
    )

    print(
        f"{planet_name}: {longitude:.6f}"
    )
from app.astrology.engine.signs import (
    tropical_to_sidereal,
    get_sign
)



