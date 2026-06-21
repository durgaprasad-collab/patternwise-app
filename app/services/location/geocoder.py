from functools import lru_cache

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

geolocator = Nominatim(
    user_agent="PatternWise/1.0 (https://patternwise.in; admin@patternwise.in)",
    timeout=8,
)
geocode = RateLimiter(
    geolocator.geocode,
    min_delay_seconds=1,
    swallow_exceptions=True,
)

@lru_cache(maxsize=512)
def search_city(city: str):

    search_text = city.strip()
    if len(search_text) < 3:
        return []

    locations = geocode(
        search_text,
        exactly_one=False,
        limit=5,
        addressdetails=True
    )

    results = []

    if not locations:
        return []

    for loc in locations:

        results.append({
            "name": loc.address,
            "latitude": loc.latitude,
            "longitude": loc.longitude
        })

    return results
