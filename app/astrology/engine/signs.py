SIGNS = [
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces"
]


def tropical_to_sidereal(longitude, ayanamsa):
    sidereal = longitude - ayanamsa

    if sidereal < 0:
        sidereal += 360

    return sidereal


def get_sign(longitude):
    sign_index = int(longitude // 30)
    return SIGNS[sign_index]