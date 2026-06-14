from app.astrology.services.chart_generator import ChartGenerator
from app.astrology.services.chart_repository import ChartRepository

chart = ChartGenerator.generate_d1(
    1987,
    4,
    29,
    12.5
)

saved = ChartRepository.save_chart(
    profile_id=1,
    chart_system="vedic",
    ayanamsa="lahiri",
    chart_json=chart
)

print("Saved Chart ID:", saved.id)