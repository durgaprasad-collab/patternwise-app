from pprint import pprint

from app.astrology.engine import ayanamsa
from app.astrology.engine.nakshatra import get_nakshatra, get_pada
from app.astrology.engine.signs import get_sign, tropical_to_sidereal
from app.astrology.engine.signs import get_sign
from app.astrology.services.chart_generator import (
    ChartGenerator
)

chart = ChartGenerator.generate_d1(
    1987,
    4,
    29,
    12.5
)
from app.astrology.ephemeris.swiss import SwissEphemeris
from app.astrology.engine.houses import get_house_signs

jd = SwissEphemeris.calculate_julian_day(1987, 4, 29, 12.5)

asc = SwissEphemeris.get_ascendant(
    jd,
    13.0008413,
    80.2023035
)
ayanamsa = SwissEphemeris.get_lahiri_ayanamsa(jd)
asc_sidereal = tropical_to_sidereal(
    asc,
    ayanamsa
)

from pprint import pprint

pprint(chart["houses"])

print("Asc Tropical:", asc)
print("Asc Sidereal:", asc_sidereal)
print("Asc Sign:", get_sign(asc_sidereal))
print("Asc Nakshatra:", get_nakshatra(asc_sidereal))
print("Asc Pada:", get_pada(asc_sidereal))