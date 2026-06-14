NAKSHATRAS = [
    "Ashwini",
    "Bharani",
    "Krittika",
    "Rohini",
    "Mrigashira",
    "Ardra",
    "Punarvasu",
    "Pushya",
    "Ashlesha",
    "Magha",
    "Purva Phalguni",
    "Uttara Phalguni",
    "Hasta",
    "Chitra",
    "Swati",
    "Vishakha",
    "Anuradha",
    "Jyeshta",
    "Mula",
    "Purva Ashadha",
    "Uttara Ashadha",
    "Shravana",
    "Dhanishta",
    "Shatabhisha",
    "Purva Bhadrapada",
    "Uttara Bhadrapada",
    "Revati"
]


def get_nakshatra(longitude):

    nakshatra_size = 13.3333333333

    index = int(longitude // nakshatra_size)

    return NAKSHATRAS[index]


def get_pada(longitude):

    nakshatra_size = 13.3333333333

    pada_size = nakshatra_size / 4

    remainder = longitude % nakshatra_size

    return int(remainder // pada_size) + 1