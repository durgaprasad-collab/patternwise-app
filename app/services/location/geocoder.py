from geopy.geocoders import Nominatim

geolocator = Nominatim(
    user_agent="patternwise"
)

def search_city(city: str):

    locations = geolocator.geocode(
        city,
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