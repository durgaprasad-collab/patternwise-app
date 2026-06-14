import swisseph as swe

from app.astrology.engine import houses


class SwissEphemeris:

    @staticmethod
    def set_lahiri():
        swe.set_sid_mode(swe.SIDM_LAHIRI)

    @staticmethod
    def get_lahiri_ayanamsa(jd):
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        return swe.get_ayanamsa_ut(jd)
    
    @staticmethod
    def get_sun_longitude(jd):
        result = swe.calc_ut(jd, swe.SUN)
        return result[0][0]
    
    @staticmethod
    def calculate_julian_day(
        year: int,
        month: int,
        day: int,
        hour_decimal: float
    ):
        return swe.julday(
            year,
            month,
            day,
            hour_decimal
        )
    
    @staticmethod
    def get_planet_longitude(jd, planet_id):
        result = swe.calc_ut(jd, planet_id)
        return result[0][0]

    @staticmethod
    def get_ascendant(
        jd,
        latitude,
        longitude
    ):
        houses = swe.houses(
            jd,
            latitude,
            longitude,
            b'P'
        )

        ascendant = houses[1][0]
        return ascendant