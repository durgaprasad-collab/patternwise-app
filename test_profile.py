from pprint import pprint

from app.astrology.profile.profile_builder import (
    ProfileBuilder
)

chart = {
    "ascendant": {
        "sign": "Libra",
        "nakshatra": "Swati"
    },

    "planets": {
        "Moon": {
            "sign": "Leo",
            "nakshatra": "Purva Phalguni"
        }
    }
}

profile = ProfileBuilder.build(chart)

pprint(profile)