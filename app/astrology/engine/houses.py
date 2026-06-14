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


def get_house_signs(ascendant_sign):

    start = SIGNS.index(
        ascendant_sign
    )

    houses = {}

    for i in range(12):

        houses[i + 1] = SIGNS[
            (start + i) % 12
        ]
    
    return houses