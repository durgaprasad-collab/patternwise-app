from app.astrology.ephemeris.swiss import SwissEphemeris
from app.astrology.engine.planets import PLANETS
from app.astrology.engine.nodes import calculate_ketu
from app.astrology.engine.houses import ( get_house_signs)

from app.astrology.engine.signs import (
    tropical_to_sidereal,
    get_sign
)
from app.astrology.engine.nakshatra import (
    get_nakshatra,
    get_pada
)


class ChartGenerator:

    @staticmethod
    def generate_d1(
        year,
        month,
        day,
        hour_decimal,
        latitude,
        longitude
    ):

        jd = SwissEphemeris.calculate_julian_day(
            year,
            month,
            day,
            hour_decimal
        )

        ayanamsa = SwissEphemeris.get_lahiri_ayanamsa(
            jd
        )

        chart = {"chart_system": "vedic",
            "ayanamsa": "lahiri",
            "ascendant": {},
            "houses": {},
            "planets": {}
            }
        
        asc = SwissEphemeris.get_ascendant(
    jd,
    latitude,
    longitude
)
        asc_sidereal = tropical_to_sidereal(
            asc,
            ayanamsa
)
        chart["ascendant"] = {
                "tropical": round(asc, 6),
                "sidereal": round(asc_sidereal, 6),
                "sign": get_sign(asc_sidereal),
                "nakshatra": get_nakshatra(asc_sidereal),
                "pada": get_pada(asc_sidereal)
            } 

        chart["houses"] = get_house_signs(
    chart["ascendant"]["sign"]
)
        for planet_name, planet_id in PLANETS.items():

            tropical = SwissEphemeris.get_planet_longitude(
                jd,
                planet_id
            )

            sidereal = tropical_to_sidereal(
                tropical,
                ayanamsa
            )

            chart["planets"][planet_name] = {
                "tropical": round(tropical, 6),
                "sidereal": round(sidereal, 6),
                "sign": get_sign(sidereal),
                "nakshatra": get_nakshatra(
                    sidereal
                ),
                "pada": get_pada(
                    sidereal
                )
            }
            
           


       
            # Calculate Ketu based on Rahu's position
        rahu_tropical = chart["planets"]["Rahu"]["tropical"]
        ketu_tropical = calculate_ketu(rahu_tropical)
        ketu_sidereal = tropical_to_sidereal(ketu_tropical, ayanamsa)
        chart["planets"]["Ketu"] = {
            "tropical": round(ketu_tropical, 6),
            "sidereal": round(ketu_sidereal, 6),
            "sign": get_sign(ketu_sidereal),
            "nakshatra": get_nakshatra(ketu_sidereal),
            "pada": get_pada(ketu_sidereal)
        }

        return chart