from .models import CosmicAlignmentProfile

from .core_gifts import ASCENDANT_GIFTS
from .growth_edges import ASCENDANT_GROWTH_EDGES
from .untapped_potential import ASCENDANT_POTENTIAL
from .energy_drains import ASCENDANT_DRAINS

from app.astrology.knowledge.moon_signs import MOON_SIGN_TRAITS
from app.astrology.knowledge.nakshatras import NAKSHATRA_TRAITS

from .alignment_score import AlignmentScoreCalculator
class ProfileBuilder:

    @classmethod
    def build(cls, chart_json):

        asc_sign = chart_json["ascendant"]["sign"]
        print("ASC SIGN:", repr(asc_sign))

        print("GIFTS:", ASCENDANT_GIFTS.get(asc_sign))
        print("EDGES:", ASCENDANT_GROWTH_EDGES.get(asc_sign))
        print("POTENTIAL:", ASCENDANT_POTENTIAL.get(asc_sign))
        print("DRAINS:", ASCENDANT_DRAINS.get(asc_sign))
        asc_nakshatra = chart_json["ascendant"]["nakshatra"]

        moon_sign = chart_json["planets"]["Moon"]["sign"]
        moon_nakshatra = chart_json["planets"]["Moon"]["nakshatra"]

        gifts = list(ASCENDANT_GIFTS.get(
            asc_sign,
            []
        ))

        edges = list(ASCENDANT_GROWTH_EDGES.get(
            asc_sign,
            []
        ))

        potential = list(ASCENDANT_POTENTIAL.get(
            asc_sign,
            []
        ))

        drains = list(ASCENDANT_DRAINS.get(
            asc_sign,
            []
        ))  

        moon_data = MOON_SIGN_TRAITS.get(moon_sign, {})
        gifts.extend(moon_data.get("emotional_strengths", []))
        drains.extend(moon_data.get("emotional_challenges", []))
        asc_nakshatra_data = NAKSHATRA_TRAITS.get(asc_nakshatra, {})
        gifts.extend(asc_nakshatra_data.get("gifts", []))
        moon_nakshatra_data = NAKSHATRA_TRAITS.get(moon_nakshatra, {})
        gifts.extend(moon_nakshatra_data.get("gifts", []))

        edges.extend(
        asc_nakshatra_data.get(
            "growth",
            []
        )
    )

        edges.extend(
        moon_nakshatra_data.get(
            "growth",
            []
        )
    )
        gifts = sorted(
        list(set(gifts))
    )

        edges = sorted(
        list(set(edges))
    )

        drains = sorted(
        list(set(drains))
    )

        potential = sorted(
        list(set(potential))
    )
        return CosmicAlignmentProfile(
            core_gifts=gifts,
            growth_edges=edges,
            untapped_potential=potential,
            energy_drains=drains,
            alignment_score=AlignmentScoreCalculator.calculate(
                gifts,
                potential,
                edges,
                drains
            )
        )
