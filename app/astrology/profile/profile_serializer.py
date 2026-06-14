def serialize_profile(profile):

    return {
        "core_gifts": profile.core_gifts,
        "growth_edges": profile.growth_edges,
        "untapped_potential": profile.untapped_potential,
        "energy_drains": profile.energy_drains,
        "natural_potential_index": profile.alignment_score
    }