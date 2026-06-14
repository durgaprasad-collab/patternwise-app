from app.astrology.services.chart_service import ChartService

chart = ChartService.generate_and_save_chart(1)

print("Saved Chart ID:", chart.id)